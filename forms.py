from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from flask_ckeditor.fields import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    intro = StringField("Intro", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    img_url = StringField('Image', validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# RegisterForm to register new users
class RegisterForm(FlaskForm):
    name = StringField("Nome:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Confirmar!")


# SubscribeForm to get users emails
class SubscribeForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    submit = SubmitField("Receber Newsletter!")


# LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Entrar!")


# CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment_text = TextAreaField("Deixa o seu comentário abaixo", validators=[DataRequired()], render_kw={"rows": 5, "cols": 30})
    submit = SubmitField("Enviar!")


# CategoryForm so users can leave comments below posts
class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField("add category!")


# ContactForm so users can contact us
class ContactForm(FlaskForm):
    name = StringField("Nome:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    message = TextAreaField("Mensagem:", validators=[DataRequired()], render_kw={"rows": 7, "cols": 30})