from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Form handling route
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')
    return render_template('result.html', name=name, age=age)

# if __name__ == '__main__':
#     app.run(debug=True)

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
#     return "<p>BigID, Welcome.project done!</p>"

# @app.route("/health")
# def health():
#     return jsonify(
#         status="UP"
#     )
# @app.route("/details")
# def details():
#     hostname, ip = fetchDetails()
#     return render_template('index.html', HOSTNAME=hostname, IP=ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
