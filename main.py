from datetime import date, datetime
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import func

# import forms.py

# import db.py


# FLASK CONFIGURATION
app = Flask(__name__)
#app.config['SECRET_KEY'] = '8BYkEfBA6O6donTGtgK86gTihBXox7C0sKR6b'
# ckeditor = CKEditor(app)
Bootstrap5(app)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

