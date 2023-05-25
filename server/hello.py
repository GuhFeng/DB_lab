# py -m flask --app hello run --debug
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session encryption


def log_the_user_in(username):
    # Perform necessary actions to log the user in
    # This could include setting session variables, generating tokens, etc.
    session['username'] = username

def getuid(username):
    return 1

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
    posts = get_recent_posts()
    # show the user profile for that user
    return render_template('posts.html', posts=posts)

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
    return render_template('users.html', users=users)

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
