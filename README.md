EOW Ltd. is a dynamic e-commerce platform developed as a capstone project for the Web Development for Information Systems course

Individual contributions:
Mohammed Faisal: Admin Panel and Management
•	Tasks: Admin login, dashboard with stats, product/category CRUD, user management, admin setup script.
•	Files: admin_routes.py, create_admin.py, config.py, run.py.
•	Templates: Admin HTML (All Files in app>templates>admin).

Annas Naiz: User Authentication and Profile Management
•	Tasks: Signup, login with 2FA, logout, profile updates (username, picture, 2FA settings).
•	Files: routes.py (auth/profile routes, 2FA route, contact, about), forms.py (LoginForm, SignupForm, TwoFactorForm, ProfileForm), models.py (User), utils.py (2FA).
•	Templates: Auth/profile HTML (login.html, profile.html, signup.html, two_factor.html, base.html, about.html, contact.html).

Muhammad Farhan Rafique: Shopping Functionality and Order Processing
•	Tasks: Home page with products, product details, search, cart management, checkout with email confirmation, static pages.
•	Files: routes.py (add_to_cart, cart, checkout, order_placed, search, clear_cart, /), forms.py (ProductForm, CheckoutForm, CategoryForm), models.py (Product, Order, OrderItem, Category), utils.py (email).
•	Templates: Shopping HTML (home.html, cart.html, checkout.html, order_placed.html, product.detail.html).
