# py -m flask --app hello run --debug
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, request
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import SQL.utils as util

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session encryption


def log_the_user_in(username):
    # Perform necessary actions to log the user in
    # This could include setting session variables, generating tokens, etc.
    session['username'] = username


def getuid(username):
    if username == 'admin':
        return 1
    else:
        return 0


@app.route('/')
def home():
    username = session.get('username')  # Retrieve username from session
    return render_template('main.html',
                           uid=getuid(username),
                           username=username,
                           title='首页')


@app.route('/user/<uid>')
def show_user_profile(uid):
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    user_info = util.get_user_info_by_uid(uid)
    user_info = {k: v[0] for k, v in user_info.items()}
    # show the user profile for that user
    return render_template('user.html', user_info=user_info, title='用户信息')


@app.route('/post/<pid>')
def show_post(pid):
    print(pid)
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    post_info = util.get_post_info_by_pid(pid)
    reply = util.get_comment_info_by_pid(2)
    print(reply)
    post_info = {k: v[0] for k, v in post_info.items()}
    reply_info = {
        f'reply{i}': {
            'Time': reply['Comment_Content'][i],
            'Content': reply['Comment Time'][i]
        }
        for i in range(len(reply["Comment_Content"]))
    }
    # show the user profile for that user
    return render_template('post.html', replys=reply_info, post_info=post_info)


@app.route('/posts')
def show_posts():
    """
    posts = {
        'post1': {
            'PostTitle': '家人们谁懂啊',
            'Content': '家人们谁懂啊家人们谁懂啊家人们谁懂啊家人们谁懂啊家人们谁懂啊家人们谁懂啊'
        },
        'post2': {
            'PostTitle': '松活弹抖闪电鞭',
            'Content': '一鞭，二鞭，三鞭，四鞭，五鞭，打了五鞭'
        },
        'post3': {
            'PostTitle': '鸡你太美',
            'Content': '鸡你太美！鸡你太美！鸡你实在是太美！'
        }
    }
    """
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    posts = util.get_recent_posts(5)
    posts = {
        f'post{i}': {
            'PostTitle': posts['PostTitle'][i],
            'Content': posts['Content'][i],
            'ID': posts['Post ID'][i]
        }
        for i in range(len(posts["Content"]))
    }
    username = session.get('username')
    return render_template('posts.html',
                           posts=posts,
                           uid=getuid(username),
                           title='最新帖子')


@app.route('/users')
def show_users():
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    users = {
        'user1': {
            'username': 'JohnDoe',
            'age': 25,
            'email': 'johndoe@example.com'
        },
        'user2': {
            'username': 'JaneSmith',
            'age': 30,
            'email': 'janesmith@example.com'
        },
        'user3': {
            'username': 'BobJohnson',
            'age': 35,
            'email': 'bobjohnson@example.com'
        }
    }
    username = session.get('username')
    return render_template('users.html',
                           users=users,
                           uid=getuid(username),
                           title='我的关注')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print("login {} {}".format(username, password))

    # Check if the username and password match a database record
    # For the sake of simplicity, let's assume a hardcoded username and password
    valid_username = "admin"
    valid_password = "password"

    if username == valid_username and password == valid_password:
        log_the_user_in(username)  # Call the login function
        return jsonify(success=True)
    else:
        return jsonify(error="用户名或密码不正确")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    print("signup {} {}".format(username, password))
    # Store it in database
    return jsonify(success=True)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
    util.close_conn()
