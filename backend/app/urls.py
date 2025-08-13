from .views import api_bp
from . import models

# Additional URL routes
def register_routes(app):
    @app.route('/')
    def health_check():
        return jsonify({"status": "healthy"})
    
    # Admin routes
    @app.route('/admin/agents')
    @admin_required
    def admin_agents():
        agents = models.AIAgent.query.all()
        return jsonify([agent.to_dict() for agent in agents])
    
    # Add more routes as needed

# Error handlers
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal server error"}), 500
