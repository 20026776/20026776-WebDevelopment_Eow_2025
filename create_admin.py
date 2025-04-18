from app import create_app, db
from app.models import User
import getpass

app = create_app()

with app.app_context():
    email = input("Enter admin email address: ").strip()
    if not email:
        print("Email cannot be empty!")
        exit(1)

    password = getpass.getpass("Enter admin password: ")
    confirm = getpass.getpass("Repeat admin password: ")
    if password != confirm:
        print("Passwords do not match!")
        exit(1)

    admin = User.query.filter_by(email=email).first()
    if not admin:
        username = email.split('@')[0]
        admin = User(email=email, username=username)
        admin.set_password(password)
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        print("Admin account created successfully!")
    else:
        admin.set_password(password)
        admin.is_admin = True
        db.session.commit()
        print("Admin account updated successfully!")
