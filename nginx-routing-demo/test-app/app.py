from flask import Flask, request
app = Flask(__name__, static_url_path='')

@app.route('/test')
def hello_world_test():
    return '/test Dockerized Test Application. No arguments'

@app.route('/test/<name>')
def dev_name(name):
    return '/test Dockerized Development Application, Hello %s' % name

@app.route('/test/colors')
def colors():
    return app.send_static_file('colors.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
