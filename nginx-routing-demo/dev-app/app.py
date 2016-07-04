from flask import Flask, request
app = Flask(__name__)

@app.route('/dev')
def hello_world_dev():
    return '/dev Dockerized Development Application. No arguments'

@app.route('/dev/<name>')
def dev_name(name):
    return '/dev Dockerized Development Application, Hello %s' % name

@app.route('/dev/cities')
def cities():
    return app.send_static_file('cities.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
