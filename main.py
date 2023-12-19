from datetime import date, datetime
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib

# import forms.py
from forms import CommentForm, ContactForm, CategoryForm, CreatePostForm, LoginForm, RegisterForm, SubscribeForm

#import db.py
from db import db, User, BlogPost, Subscribe, Comment, Category, init_db


# FLASK CONFIGURATION
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donTGtgK86gTihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
ckeditor = CKEditor(app)
Bootstrap5(app)

# load db config
init_db(app)


# Create an instance of LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view endpoint


# LOGIN USER
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# ADMIN DECORATOR FUNCTION
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the current user is logged in and has ID 1
        if current_user.id == 1:
            return func(*args, **kwargs)
        else:
            abort(403)  # HTTP 403 Forbidden error

    return decorated_function


@app.route('/')
def home():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/blog')
def blog():
    # Fetch all unique categories
    categories = db.session.query(Category.name).distinct().all()
    categories = [category[0] for category in categories]

    # Fetch all posts
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()

    return render_template("blog.html", all_posts=posts, all_categories=categories, current_user=current_user)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    # current post
    requested_post = db.get_or_404(BlogPost, post_id)

    return render_template("post.html", post=requested_post, current_user=current_user)


@app.route('/new_post', methods=['GET', 'POST'])
@admin_only
def create_post():
    form = CreatePostForm()
    # fetch all categories
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    # fetch data from form
    if form.validate_on_submit():
        # Retrieve the selected category
        selected_category_id = form.category.data
        selected_category = Category.query.get(selected_category_id)

        new_post = BlogPost(
            title=form.title.data,
            intro=form.intro.data,
            slug=form.slug.data,
            img_url=form.img_url.data,
            body=form.body.data,
            author=current_user,
            category=selected_category,
            date=date.today().strftime("%B %d, %Y"),
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('blog'))

    return render_template("new_post.html", form=form, current_user=current_user)


@app.route('/category')
def blog_category():
    return render_template("blog_category.html")


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        # check if already registerd
        email = form.email.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        # hash and salt password
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            name = form.name.data,
            email = form.email.data,
            password = hash_and_salted_password,
        )

        # commit changes
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)

        return redirect(url_for('home'))

    return render_template("sign_up.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # retrieve data from form
        email = form.email.data
        password = form.password.data

        # find user in User DB by email entered
        result = db.session.execute(db.Select(User).where(User.email == email))
        user = result.scalar()

        # check if login details are correct
        if not user:
            flash("Email não encontrado, tente novamente.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Senha incorreta, tente novamente.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    # if methods == GET
    return render_template("login.html", form=form)


@app.route('/contato')
def contato():
    return render_template("contato.html")


@app.route('/sobre-nos')
def sobre_nos():
    return render_template("sobre-nos.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

