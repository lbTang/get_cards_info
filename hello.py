from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import datetime

from werkzeug.utils import redirect

app = Flask(__name__)


@app.route('/<name>')
def hello(name):
    if not name:
        name='tang'
    return render_template('hello.html',name=name)


if __name__ == "__main__":
    app.run(debug=True)

