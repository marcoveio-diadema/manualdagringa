from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
from sqlalchemy import event
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib


# import forms.py
from forms import CommentForm, ContactForm, CategoryForm, CreatePostForm, LoginForm, RegisterForm, SubscribeForm, SearchForm, QuestionsForm


# FLASK CONFIGURATION
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET-KEY-HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# CK EDITOR AND BOOTSTRAP
ckeditor = CKEditor(app)
Bootstrap5(app)


# MODELS
# user model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

    def __repr__(self):
        return '<Name %r>' % self.name
    
    # Add the is_admin property
    @property
    def is_admin(self):    
        return self.id == 1 


# new post model
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")

    title = db.Column(db.String(150), unique=True, nullable=False)
    intro = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    body_2 = db.Column(db.Text, nullable=False)
    img_background = db.Column(db.String(500), nullable=False)
    img_1 = db.Column(db.String(500), nullable=False)
    img_2 = db.Column(db.String(500), nullable=False)
    img_3 = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    @property
    def author_name(self):
        return self.user.name if self.user else None
    


# comments model
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Child relationship with the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child relationship with the tablename of BlogPost.
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")

# category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


# subscribe model
class Subscribe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# questions model
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150), unique=True, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# create db
with app.app_context():
    db.create_all()


# Create an instance of LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view endpoint

# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=200,
                    rating='g',
                    default='robohash',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# LOGIN USER
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



# ADMIN DECORATOR FUNCTION
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the current user is logged in and has ID 1
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        else:
            abort(403)  # HTTP 403 Forbidden error

    return decorated_function

#INDEX
@app.route('/', methods=['GET', 'POST'])
def home():
    form = SubscribeForm()
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()

    return render_template("index.html", all_posts=posts, current_user=current_user, form=form)

# BLOG 
@app.route('/blog')
def blog():
    # Fetch all unique categories
    categories = db.session.query(Category.name).distinct().all()
    categories = [category[0] for category in categories]

    # Fetch all posts
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()

    # subscribe form
    subscribe_form = SubscribeForm()

    return render_template("blog.html", all_posts=posts, all_categories=categories, current_user=current_user, form=subscribe_form)

# SHOW POST
@app.route('/post/<int:post_id>/<slug>', methods=['GET', 'POST'])
def show_post(post_id, slug):
    # current post
    requested_post = db.get_or_404(BlogPost, post_id)
    # Check if the provided slug matches the actual slug of the post
    if requested_post.slug != slug:
        abort(404)

    # Fetch all unique categories
    categories = db.session.query(Category.name).distinct().all()
    categories = [category[0] for category in categories]

    # other posts
    other_posts = BlogPost.query.filter(BlogPost.id != post_id).order_by(BlogPost.date.desc()).all()

    # fetch comments form
    comment_form = CommentForm()
    # only allow logged-in users to comment
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Você precisa fazer o login ou se registrar para comentar nos posts.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()

        # Reset the comment text area after submitting the comment
        comment_form.comment_text.data = ''

    # Fetch comments associated with the post
    comments = Comment.query.filter_by(post_id=post_id).all()

    return render_template("post.html", post=requested_post, current_user=current_user,
                           form=comment_form, comments=comments, other_posts=other_posts, all_categories=categories)

# DELETE COMMENT
@app.route("/delete-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)

     # Default values for post_id and slug
    post_id = None
    slug = None

    if comment_to_delete:
        # Check if the current user is the author of the comment
        if current_user.is_authenticated and (current_user.id == comment_to_delete.comment_author.id or current_user.is_admin):
            parent_post = comment_to_delete.parent_post
            post_id = parent_post.id

            db.session.delete(comment_to_delete)
            db.session.commit()
            flash("Comment deleted successfully.")
    

            # Check if the delete request came from the admin template
            if "from_admin" in request.args and request.args["from_admin"] == "true":
                # Redirect back to the admin page
                return redirect(url_for("admin"))
            else:
                # Redirect back to the post page
                return redirect(url_for("show_post", post_id=post_id, slug=parent_post.slug))
        
    flash("Comment not found.")
    return redirect(url_for("home"))


# CREATE NEW POST
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
            img_background=form.img_background.data,
            slug=form.slug.data.lower().replace(" ", "-"),
            intro=form.intro.data,
            img_1=form.img_1.data,
            img_2=form.img_2.data,
            img_3=form.img_3.data,
            body=form.body.data,
            body_2=form.body_2.data,
            author=current_user,
            category=selected_category,
            date=datetime.utcnow(),
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('blog'))

    return render_template("new_post.html", form=form, current_user=current_user)

# EDIT POST
@app.route('/edit-post/<int:post_id>/<slug>', methods=['GET', 'POST'])
@admin_only
def edit_post(post_id, slug):
    post = db.get_or_404(BlogPost, post_id)

    edit_form = CreatePostForm(
        title=post.title,
        img_background=post.img_background,
        slug=post.slug,
        intro=post.intro,
        img_1=post.img_1,
        img_2=post.img_2,
        img_3=post.img_3,
        body=post.body,
        body_2=post.body_2,
        author=post.author,
        category=post.category,
    )

    # Fetch all categories
    categories = [(category.id, category.name) for category in Category.query.all()]

    # Set choices for the category field in the form
    edit_form.category.choices = categories

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.img_background = edit_form.img_background.data
        post.intro = edit_form.intro.data
        post.slug = edit_form.slug.data
        post.img_1 = edit_form.img_1.data
        post.img_2 = edit_form.img_2.data
        post.img_3 = edit_form.img_3.data
        post.author = current_user
        post.body = edit_form.body.data
        post.body_2 = edit_form.body_2.data

        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id, slug=post.slug))
    return render_template("new_post.html", form=edit_form, is_edit=True, current_user=current_user, categories=categories, slug=post.slug)

# DELETE POST
@app.route('/delete-post/<int:post_id>')
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('blog'))

# CONTEXT FUNCTION FOR SEARCH
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# SEARCH FOR A POST
@app.route('/busca', methods=['POST'])
def search():
    form = SearchForm()

    # Fetch all unique categories
    categories = db.session.query(Category.name).distinct().all()
    categories = [category[0] for category in categories]

    # search in the database:
    posts_query = BlogPost.query

    if form.validate_on_submit():
        # get data from submitted form
        busca = form.busca.data

        # query the database
        posts = posts_query.filter(BlogPost.body.like('%' + busca + '%')).order_by(BlogPost.title).all()

        return render_template("search.html", form=form, busca=busca, posts=posts, all_categories=categories)

# POSTS PER CATEGORY
@app.route('/category/<category_name>')
def post_category(category_name):
    # Fetch all unique categories
    categories = db.session.query(Category.name).distinct().all()
    categories = [category[0] for category in categories]

    category = Category.query.filter_by(name=category_name).first()
    # if no category
    if category is None:
        abort(404)  # or handle the case where the category is not found

    # Fetch posts that belong to the selected category
    posts = BlogPost.query.filter_by(category=category).all()

    return render_template("blog_category.html", posts=posts, category_name=category_name, current_user=current_user, all_categories=categories)


# FORUM
@app.route('/forum')
def forum():
    return render_template("forum_index.html")


# FAQS PAGE
@app.route('/perguntas-frequentes', methods=['GET', 'POST'])
def faqs():
    form = QuestionsForm()

    questions = Questions.query.all()

    if form.validate_on_submit():
        # check if already registerd
        question = form.question.data
        result = db.session.execute(db.select(Questions).where(Questions.question == question))
        double_question = result.scalar()

        if double_question:
            # User already exists
            flash("Pergunta ja cadastrada, tente outra.")
            return redirect(url_for('faqs'))

        new_question = Questions(
            question = form.question.data,
            answer = form.answer.data,
        )

         # commit changes
        db.session.add(new_question)
        db.session.commit()

        # message to confirm
        flash("Pergunta adicionada com sucesso!")
        return redirect(url_for('faqs'))

    return render_template('faqs.html', form=form, questions=questions)

# DELETE CATEOGRY
@app.route('/delete-category/<int:category_id>')
@admin_only
def delete_category(category_id):
    category_to_delete = db.get_or_404(Category, category_id)
    db.session.delete(category_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))


# REGISTER ROUTE
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
            flash("Email ja cadastrado, faça o seu login.")
            return redirect(url_for('login'))

        # hash and salt password
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            password = hash_and_salted_password,
        )

        # commit changes
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)

        flash("Bem vindo a nossa comunidade!")
        return redirect(url_for('user', user_id=new_user.id, name=current_user.name))

    return render_template("sign_up.html", form=form)

# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # retrieve data from form
        username = form.username.data
        password = form.password.data

        # find user in User DB by email entered
        result = db.session.execute(db.Select(User).where(User.username == username))
        user = result.scalar()

        # check if login details are correct
        if not user:
            flash("Usuario não encontrado, tente novamente.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Senha incorreta, tente novamente.")
            return redirect(url_for('login'))
        else:
            login_user(user)

             # Redirect based on user ID
            if user.id == 1:  # Admin user ID, adjust as needed
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user', user_id=user.id, name=current_user.name))
            
    # if methods == GET
    return render_template("login.html", form=form)



# USER PAGE
@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
     # get users database
    user = db.get_or_404(User, user_id)

    # get register form
    edit_user_form = RegisterForm(
        email = user.email,
        name = user.name,
        username = user.username,
        password = user.password,
    )

    if edit_user_form.validate_on_submit():

         # hash and salt password
        hash_and_salted_edited_password = generate_password_hash(
            edit_user_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        user.email = edit_user_form.email.data
        user.name = edit_user_form.name.data
        user.username = edit_user_form.data
        user.password = hash_and_salted_edited_password


        # save changes to db
        db.session.commit()

        # message to confirm update
        flash('Dados atualizados com sucesso!')
        return redirect( url_for('user', user_id=user.id))
    
    return render_template("user.html", form=edit_user_form, current_user=current_user, name=current_user.name, gravatar=gravatar)


# DELETE USER
@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    # fetch user to be deleted
    user_to_delete = db.get_or_404(User, user_id)

    # Only administrators can delete other users
    if current_user.is_admin and current_user.id != user_to_delete.id:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully!')
        return redirect(url_for('admin'))
    
    # Users can delete their own account
    elif current_user.id == user_to_delete.id:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Que pena te ver partir, volte quando quiser!')

         # Log out the user after deleting the account
        logout_user()

        return redirect(url_for('home'))
    
    # If it's neither an admin deleting another user nor a user deleting their own account, return a forbidden error
    else:
        abort(403)


# DELETE SUBSCRIBER
@app.route('/delete-subscriber/<int:subscriber_id>')
@admin_only
def delete_subscriber(subscriber_id):
    subscriber_to_delete = db.get_or_404(Subscribe, subscriber_id)
    db.session.delete(subscriber_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/delete-question/<int:question_id>')
@admin_only
def delete_question(question_id):
    question_to_delete = db.get_or_404(Questions, question_id)
    db.session.delete(question_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))


# NEWSLETTER SUBSCRIBE ROUTE
@app.route('/subscribe', methods=['POST', 'GET'])
def subscribe():
    # fetch all posts
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()

    # form
    form = SubscribeForm()

    if form.validate_on_submit():
        # check if already registerd
        email = form.email.data
        result = db.session.execute(db.select(Subscribe).where(Subscribe.email == email))
        subscribed_user = result.scalar()

        if subscribed_user:
            # User already exists
            flash("Email já esta cadastrado, use outro!")
            return redirect(url_for('subscribe'))

        # Create a new Names instance and add it to the database
        new_subscriber = Subscribe(
            email=form.email.data
        )

        db.session.add(new_subscriber)
        db.session.commit()
        flash("Email cadastrado com sucesso!")
        return redirect(url_for('home'))
    return render_template("index.html", form=form, all_posts=posts)


# CONTACT ROUTE

MY_EMAIL = "MY_EMAIL"
MY_PASSWORD = "MY_PASSWORD"


@app.route('/contato', methods=['POST', 'GET'])
def contato():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        flash("Obrigado pela mensagem, responderemos em breve!")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="OTHER_EMAIL",
                msg=f"Subject:Novo contato! \n\n Email sent by:{name}\nEmail:{email}\nMensagem:\n{message}")

    return render_template("contato.html")


@app.route('/sobre-nos')
def sobre_nos():
    return render_template("sobre-nos.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# ADMIN ROUTE:
@app.route('/admin', methods=['GET', 'POST'])
@admin_only
def admin():
     # Fetch all comments
    comments = Comment.query.all()

    # fetch all posts
    posts = BlogPost.query.all()

    # fetch all users
    users = User.query.all()

    # fetch all subscribers
    subscribers = Subscribe.query.all()

    # fetch all categories
    categories = Category.query.all()

    # fetch all questions
    questions = Questions.query.all()

     # Create a form for adding a new category
    form = CategoryForm()

    if form.validate_on_submit():
         # Check if the category already exists
        existing_category = Category.query.filter_by(name=form.name.data).first()
        if existing_category:
            flash('Category already exists.', 'danger')
        else:
            # Add a new category if it doesn't exist
            new_category = Category(name=form.name.data)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template("admin.html", questions=questions, posts=posts, users=users, subscribers=subscribers, comments=comments, categories=categories, form=form)

# CUSTOM ERROR PAGES:

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Internal server error
@app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html"), 403



if __name__ == '__main__':
    app.run(debug=True)



