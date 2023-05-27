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
    if username == None:
        return 0
    return int(util.get_user_info_by_name(username)["User ID"][0])


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
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    post_info = util.get_post_info_by_pid(pid)
    reply = util.get_comment_info_by_pid(pid)
    user_id = reply["User ID"]
    user_names = [
        util.get_user_info_by_uid(uid)['User Name'][0] for uid in user_id
    ]
    post_info = {k: v[0] for k, v in post_info.items()}
    post_info['User'] = util.get_user_info_by_uid(
        post_info['User ID'])['User Name'][0]
    reply_info = {
        f'reply{i}': {
            'Time': reply['Comment_Content'][i],
            'Content': reply['Comment Time'][i],
            'User': user_names[i]
        }
        for i in range(len(reply["Comment_Content"]))
    }
    # show the user profile for that user
    return render_template('post.html',
                           replys=reply_info,
                           post_info=post_info,
                           pid=pid,
                           uid=currentid)


@app.route('/posts')
def show_posts():
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    posts = util.get_recent_posts(100)
    user_id = posts["User ID"]
    user_names = [
        util.get_user_info_by_uid(uid)['User Name'][0] for uid in user_id
    ]
    posts = {
        f'post{i}': {
            'PostTitle': posts['PostTitle'][i],
            'Content': posts['Content'][i],
            'ID': posts['Post ID'][i],
            'time': posts['Post time'][i],
            'User': user_names[i]
        }
        for i in range(len(posts["Content"]))
    }
    username = session.get('username')
    return render_template('posts.html',
                           posts=posts,
                           uid=getuid(username),
                           title='最新帖子')


@app.route('/postnew1', methods=['GET'])
def postnew1():
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    username = session.get('username')
    return render_template('posts.html', uid=getuid(username), title='发帖')


def add_post(a, b, c):
    return util.add_post({"Content": b, "PostTitle": a, "User ID": c})


@app.route('/postnew', methods=['POST'])
def postnew():
    username = session.get('username')
    uid = getuid(username)
    title = request.json.get('title')
    content = request.json.get('content')
    pid = add_post(title, content, uid)
    return jsonify(success=True, pid=pid)


@app.route('/reply', methods=['POST'])
def reply():
    uid = request.json.get('uid')
    pid = request.json.get('pid')
    content = request.json.get('replyText')
    print(uid, pid, content)
    util.add_comment({
        "User ID": uid,
        "Post ID": pid,
        "Comment_Content": content
    })
    return jsonify(success=True, pid=pid)


@app.route('/users')
def show_users():
    currentid = getuid(session.get('username'))
    if currentid == 0:
        return render_template('visitor.html')
    users = util.get_following(22)
    ks = users.keys()
    users = {
        f'user{i}': {k: users[k][i]
                     for k in ks}
        for i in range(len(users["User ID"]))
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
    user_info = util.get_user_info_by_name(username)
    check_name, check_pass = util.remove_special_characters(
        username), util.remove_special_characters(password)
    if username != check_name or check_pass != password:
        return jsonify(error="输入不能包含特殊字符")
    if len(username) > 20 or len(password) > 20:
        return jsonify(error="输入太长")
    # Check if the username and password match a database record
    # For the sake of simplicity, let's assume a hardcoded username and password
    if len(user_info['User ID']
           ) != 0 and password == user_info['Password'][0].split(' ')[0]:
        log_the_user_in(username)  # Call the login function
        return jsonify(success=True)
    else:
        return jsonify(error="用户名或密码不正确")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    print("signup {} {}".format(username, password))
    check_name, check_pass = util.remove_special_characters(
        username), util.remove_special_characters(password)
    if username != check_name or check_pass != password:
        return jsonify(error="输入不能包含特殊字符")
    if len(username) > 20 or len(password) > 20:
        return jsonify(error="输入太长")
    util.user_register({'User Name': username, 'Password': password})
    # Store it in database
    log_the_user_in(username)
    return jsonify(success=True)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
    util.close_conn()
