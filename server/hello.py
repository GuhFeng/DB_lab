# py -m flask --app hello run --debug
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session encryption


def log_the_user_in(username):
    # Perform necessary actions to log the user in
    # This could include setting session variables, generating tokens, etc.
    session['username'] = username


@app.route('/')
def home():
    username = session.get('username')  # Retrieve username from session
    return render_template('main.html', username=username)

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
        return redirect(url_for('home', username=username))
    else:
        return "Login failed"


@app.route('/dashboard')
def dashboard():
    username = session.get('username')

    if username:
        return f"Welcome to the dashboard, {username}!"
    else:
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
