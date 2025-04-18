import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '2fa.eow@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ydkf qvmf lpcc rywf'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or '2fa.eow@gmail.com'
    
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'products')
    PROFILE_UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads', 'profile')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def create_upload_folders():
        for folder in [Config.UPLOAD_FOLDER, Config.PROFILE_UPLOAD_FOLDER]:
            os.makedirs(folder, exist_ok=True)

Config.create_upload_folders()
