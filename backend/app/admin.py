from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, AIAgent, Client, Project

admin_bp = Blueprint('admin', __name__)

class SecureModelView(ModelView):
    """Custom admin view with security"""
    def is_accessible(self):
        # Add your admin authentication logic here
        return True  # Replace with actual auth check
        
    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect(url_for('admin.login'))

def init_admin(app):
    admin = Admin(app, name='AGI Business Admin', template_mode='bootstrap3')
    
    # Add views
    admin.add_view(SecureModelView(AIAgent, db.session))
    admin.add_view(SecureModelView(Client, db.session))
    admin.add_view(SecureModelView(Project, db.session))
    
    # Custom admin views can be added here
    @admin_bp.route('/admin')
    def admin_dashboard():
        return "Admin Dashboard"
