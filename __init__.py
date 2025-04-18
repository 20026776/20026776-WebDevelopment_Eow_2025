from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask import session


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Set the login view (for @login_required)
    login_manager.login_view = 'main.login'

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin_routes import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    with app.app_context():
        db.create_all()
    

     # Context processor to inject cart_total into all templates
    @app.context_processor
    def inject_cart_total():
        cart = session.get('cart', {})
        # Sum the quantities in the cart (assumes cart is a dict: {product_id: quantity})
        total = sum(cart.values()) if cart else 0
        return dict(cart_total=total)
    
    @app.context_processor
    def inject_categories():
        from app.models import Category  # Import here to avoid circular imports
        categories = Category.query.all()
        return dict(all_categories=categories)

    return app
