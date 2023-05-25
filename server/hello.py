# py -m flask --app hello run --debug
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session encryption


def log_the_user_in(username):
    # Perform necessary actions to log the user in
    # This could include setting session variables, generating tokens, etc.
    session['username'] = username

def getuid(username):
    if username=='admin':
        return 1
    else:
        return 0

@app.route('/')
def home():
    username = session.get('username')  # Retrieve username from session
    return render_template('main.html', uid=getuid(username))

@app.route('/user/<uid>')
def show_user_profile(uid):
    user_info = get_user_info_by_uid(uid)
    # show the user profile for that user
    return render_template('user.html', user_info=user_info)

@app.route('/post/<pid>')
def show_post(pid):
    post_info = get_post_info_by_pid(pid)
    # show the user profile for that user
    return render_template('post.html', post_info=post_info)

@app.route('/posts')
def show_posts():
    posts = {
        'post1': {
            'post_title': '家人们谁懂啊',
            'post_text': '家人们谁懂啊家人们谁懂啊家人们谁懂啊家人们谁懂啊家人们谁懂啊家人们谁懂啊'
        },
        'post2': {
            'post_title': '松活弹抖闪电鞭',
            'post_text': '一鞭，二鞭，三鞭，四鞭，五鞭，打了五鞭'
        },
        'post3': {
            'post_title': '鸡你太美',
            'post_text': '鸡你太美！鸡你太美！鸡你实在是太美！'
        }
    }
    username = session.get('username')
    return render_template('posts.html', posts=posts, uid=getuid(username))

@app.route('/users')
def show_users():
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
    return render_template('users.html', users=users, uid=getuid(username))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username and password match a database record
    # For the sake of simplicity, let's assume a hardcoded username and password
    valid_username = "admin"
    valid_password = "password"

    if username == valid_username and password == valid_password:
        log_the_user_in(username)  # Call the login function
        return redirect(url_for('home'))
    else:
        return "Login failed"

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
