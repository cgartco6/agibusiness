from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .models import db, AIAgent, Client, Project
import uuid
import os
import stripe

api_bp = Blueprint('api', __name__)

# Stripe configuration
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@api_bp.route('/agents', methods=['GET'])
def list_agents():
    """List available AI agents"""
    agents = AIAgent.query.filter_by(is_active=True).all()
    return jsonify([agent.to_dict() for agent in agents])

@api_bp.route('/agent/<string:agent_id>/deploy', methods=['POST'])
def deploy_agent(agent_id):
    """Deploy a specific AI agent"""
    data = request.get_json()
    
    agent = AIAgent.query.get(agent_id)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
        
    # Create new project
    project = Project(
        client_id=data['client_id'],
        agent_id=agent.id,
        status='deploying'
    )
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        "message": f"{agent.name} deployment started",
        "project_id": project.id
    }), 202

@api_bp.route('/payment/intent', methods=['POST'])
def create_payment_intent():
    """Create Stripe payment intent"""
    data = request.get_json()
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency='zar',
            metadata={
                'client_id': data['client_id'],
                'service_type': data.get('service_type', 'general')
            }
        )
        return jsonify({
            'clientSecret': intent.client_secret
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for content creation"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"filename": filename}), 201
