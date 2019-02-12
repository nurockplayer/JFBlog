from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView


class CustomView(BaseView):
    """View function of Flask-Admin for Custom page."""

    @expose('/')
    # @login_required
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    pass
