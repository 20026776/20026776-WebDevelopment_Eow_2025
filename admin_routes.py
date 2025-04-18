from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user, login_user
from .models import Product, Category, User
from .forms import ProductForm, CategoryForm, LoginForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask import current_app


admin = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
         if not current_user.is_admin:
              abort(403)
         return f(*args, **kwargs)
    return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
         if current_user.is_admin:
              return redirect(url_for('admin.dashboard'))
         else:
              flash("You are not authorized to access the admin panel.", "danger")
              return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         if user and user.check_password(form.password.data):
              if not user.is_admin:
                  flash("You are not authorized to access the admin panel.", "danger")
              else:
                  login_user(user, remember=form.remember.data)
                  flash("Admin logged in successfully!", "success")
                  return redirect(url_for('admin.dashboard'))
         else:
              flash("Invalid email or password.", "danger")
    return render_template('admin/login.html', form=form)

@admin.route('/')
@login_required
@admin_required
def dashboard():
    product_count = Product.query.count()
    category_count = Category.query.count()
    user_count = User.query.count()
    return render_template('admin/dashboard.html', product_count=product_count,
                           category_count=category_count, user_count=user_count)

@admin.route('/products')
@login_required
@admin_required
def manage_products():
    products = Product.query.all()
    return render_template('admin/manage_products.html', products=products)

@admin.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        file = request.files['image']
        filename = 'default.jpg' 

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        product = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category.data,
            image=filename 
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin.manage_products'))

    return render_template('admin/add_product.html', form=form)

@admin.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        product.title = form.title.data
        product.description = form.description.data
        product.price = form.price.data
        product.category_id = form.category.data

        file = request.files['image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            product.image = filename 

        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.manage_products'))

    return render_template('admin/edit_product.html', form=form, product=product)


@admin.route('/products/delete/<int:product_id>')
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'info')
    return redirect(url_for('admin.manage_products'))


@admin.route('/categories')
@login_required
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/manage_categories.html', categories=categories)

@admin.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
         category = Category(name=form.name.data)
         db.session.add(category)
         db.session.commit()
         flash('Category added successfully.', 'success')
         return redirect(url_for('admin.manage_categories'))
    return render_template('admin/add_category.html', form=form)

@admin.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
         category.name = form.name.data
         db.session.commit()
         flash('Category updated successfully.', 'success')
         return redirect(url_for('admin.manage_categories'))
    return render_template('admin/edit_category.html', form=form, category=category)

@admin.route('/categories/delete/<int:category_id>')
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', 'info')
    return redirect(url_for('admin.manage_categories'))

@admin.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin.route('/users/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
         flash('You cannot delete your own account.', 'warning')
         return redirect(url_for('admin.manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'info')
    return redirect(url_for('admin.manage_users'))
