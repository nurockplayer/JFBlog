import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
# import main
from JFBlog import create_app
from JFBlog import models


# Get the ENV from os_environ
env = os.environ.get('JFBlog', 'dev')
# Create the app instance via Factory Method
app = create_app('JFBlog.config.%sConfig' % env.capitalize())

# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create new commands
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    """
    Create a python CLI.

    return: Default import object
    type: 'Dict'
    """
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Server=Server)


if __name__ == '__main__':
    manager.run()
