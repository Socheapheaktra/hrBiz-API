from flask import Flask, url_for, redirect

from routes.login import login
from routes.employee import employee
from routes.report import report
from routes.sysconfig import sysconfig

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for("login.test"))


app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(employee, url_prefix="/employee")
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(sysconfig, url_prefix='/sysconfig')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
