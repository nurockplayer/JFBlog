from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_restful import Api
from flask_login import LoginManager

# Create the Flask-Bcrypt's instance
bcrypt = Bcrypt()
# Create the Flask-Admin's instance
flask_admin = Admin()
# Create the Flask-Restful's instance
restful_api = Api()
# Create the Flask-Login's instance
login_manager = LoginManager()


# Setup the configuration for login manager
# 1. Set the loing page.
# 2. Set the more stronger auth-protection.
# 3. Show the information when you are logging.
# 4. Set the Login Messages type as 'information'.
login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this pages.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""

    from .models import User
    return User.query.filter_by(id=user_id).first()
