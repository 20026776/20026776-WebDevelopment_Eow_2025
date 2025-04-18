from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class TwoFactorForm(FlaskForm):
    code = StringField('Enter the 2FA Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    shipping_address = StringField('Shipping Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State/Province', validators=[DataRequired()])
    zip_code = StringField('ZIP/Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    paypal_email = StringField('PayPal Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Place Order')

class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image = FileField('Product Image')
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture')
    passport = StringField('Passport Details')
    two_factor_enabled = BooleanField('Enable Two-Factor Authentication')
    submit = SubmitField('Update Profile')
