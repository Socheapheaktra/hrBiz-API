from flask import Flask
from routes.login import login
from routes.employee import employee

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(employee, url_prefix="/employee")

if __name__ == '__main__':
    app.run()
