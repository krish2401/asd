from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

# Sample user data (username: password_hash)
users = {
    'user1': generate_password_hash('password1'),
    'user2': generate_password_hash('password2')
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, jsonify, render_template
# import socket
# app = Flask(__name__)

# # Function to fetch hostname and ip 
# def fetchDetails():
#     hostname = socket.gethostname()
#     host_ip = socket.gethostbyname(hostname)
#     return str(hostname), str(host_ip)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/health")
# def health():
#     return jsonify(
#         status="UP"
#     )
# @app.route("/details")
# def details():
#     hostname, ip = fetchDetails()
#     return render_template('index.html', HOSTNAME=hostname, IP=ip)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
