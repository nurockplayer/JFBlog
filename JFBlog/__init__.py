from flask import Flask, redirect, url_for

from .models import db, User, Post, Role, Tag, BrowseVolume, Reminder
from .extensions import bcrypt, flask_admin, restful_api

from .controllers import blog, main, admin
from .controllers.admin import CustomView, CustomModelView
from .controllers.flask_restful.posts import PostApi
from .controllers.flask_restful.auth import AuthApi


def create_app(object_name):
    """Create the app instance via 'Factory Method"""

    app = Flask(__name__)

    # Set the config for app instance
    app.config.from_object(object_name)

    # Will be load the SQLALCHEMY_DATABASE_URL from config.py to db object
    db.init_app(app)

    # Init the Flask-Bcrypt via app object
    bcrypt.init_app(app)

    # Init the Flask-Admin via app object
    flask_admin.init_app(app)
    # Register view function 'CustomView' into Flask-Admin
    flask_admin.add_view(CustomView(name='Custom'))
    # Register view function 'CustomModelView' into Flask-Admin
    models = [Role, Tag, Reminder, BrowseVolume]
    for model in models:
        flask_admin.add_view(
            CustomModelView(model, db.session, category='Models')
        )

    # Define the route of restful_api
    restful_api.add_resource(
        PostApi,
        '/api/posts/',
        '/api/posts/<string:post_id>',
        endpoint='restful_api_post'
    )
    restful_api.add_resource(
        AuthApi,
        '/api/auth',
        endpoint='restful_api_auth'
    )
    restful_api.init_app(app)

    # Register the Blueprint into app object
    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(main.main_blueprint)

    return app


# import the views module
# views = __import__('views')

# if __name__ == '__main__':
#     app.run()
