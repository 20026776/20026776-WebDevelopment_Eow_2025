from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from .forms import LoginForm, SignupForm, TwoFactorForm, ProfileForm, CheckoutForm
from .models import User, Product, Category, Order, OrderItem
from . import db, mail
from flask_login import login_user, logout_user, login_required, current_user
from .utils import send_two_factor_code, generate_two_factor_code, send_order_confirmation
import os
from werkzeug.utils import secure_filename
from flask import current_app



main = Blueprint('main', __name__)

@main.route('/')
def home():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('home.html', products=products, categories=categories)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/clear_cart')
@login_required
def clear_cart():
    session['cart'] = {}
    flash('Cart has been cleared.', 'info')
    return redirect(url_for('main.cart'))


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         if user and user.check_password(form.password.data):
              if user.two_factor_enabled:
                  code = generate_two_factor_code()
                  user.two_factor_code = code
                  db.session.commit()
                  send_two_factor_code(user.email, code, mail)
                  session['2fa_user_id'] = user.id
                  flash('A verification code has been sent to your email.', 'info')
                  return redirect(url_for('main.two_factor'))
              login_user(user, remember=form.remember.data)
              flash('Logged in successfully!', 'success')
              return redirect(url_for('main.home'))
         flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
         if User.query.filter((User.email==form.email.data) | (User.username==form.username.data)).first():
             flash('User already exists', 'warning')
         else:
             user = User(email=form.email.data, username=form.username.data)
             user.set_password(form.password.data)
             db.session.add(user)
             db.session.commit()
             flash('Account created successfully! Please login.', 'success')
             return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.home'))

@main.route('/two_factor', methods=['GET', 'POST'])
def two_factor():
    form = TwoFactorForm()
    user = User.query.get(session.get('2fa_user_id'))
    if not user:
         flash('Session expired, please login again.', 'warning')
         return redirect(url_for('main.login'))
    if form.validate_on_submit():
         if form.code.data == user.two_factor_code:
              user.two_factor_code = None
              db.session.commit()
              login_user(user)
              session.pop('2fa_user_id', None)
              flash('Two‑factor authentication verified successfully!', 'success')
              return redirect(url_for('main.home'))
         flash('Invalid verification code.', 'danger')
    return render_template('two_factor.html', form=form)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.passport = form.passport.data
        current_user.two_factor_enabled = form.two_factor_enabled.data
        if form.profile_pic.data:
            file = form.profile_pic.data
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['PROFILE_UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            current_user.profile_pic = filename

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form)


@main.route('/search')
def search():
    query = request.args.get('q')
    category_id = request.args.get('category', type=int)
    products_query = Product.query
    if query:
         products_query = products_query.filter(Product.title.ilike(f'%{query}%'))
    if category_id:
         products_query = products_query.filter_by(category_id=category_id)
    products = products_query.all()
    return render_template('home.html', products=products, query=query)


@main.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Product added to cart.', 'success')
    return redirect(url_for('main.home'))

@main.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for prod_id, qty in cart.items():
         product = Product.query.get(int(prod_id))
         if product:
              items.append({'product': product, 'quantity': qty})
              total += product.price * qty
    return render_template('cart.html', items=items, total=total)

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
         flash('Your cart is empty.', 'warning')
         return redirect(url_for('main.home'))
    
    total = 0
    for prod_id, qty in cart.items():
         product = Product.query.get(int(prod_id))
         if product:
              total += product.price * qty

    form = CheckoutForm()
    if form.validate_on_submit():
         order = Order(user_id=current_user.id, total=total, status='Placed')
         db.session.add(order)
         db.session.commit()
         details = {
             'full_name': form.full_name.data,
             'shipping_address': form.shipping_address.data,
             'city': form.city.data,
             'state': form.state.data,
             'zip_code': form.zip_code.data,
             'country': form.country.data,
             'paypal_email': form.paypal_email.data
         }
         
         send_order_confirmation(form.paypal_email.data, order, details)
         
         session['cart'] = {}
         flash('Order placed successfully!', 'success')
         return redirect(url_for('main.order_placed'))
    
    return render_template('checkout.html', form=form, total=total)

@main.route('/order_placed')
@login_required
def order_placed():
    return render_template('order_placed.html')
