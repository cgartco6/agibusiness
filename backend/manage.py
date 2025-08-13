#!/usr/bin/env python
import os
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from app import create_app, db
from agents.content_creator import ContentCreatorAgent
from agents.social_poster import SocialPosterAgent
from agents.client_support import ClientSupportAgent
from agents.payment_processor import PaymentProcessorAgent
import subprocess
import threading

# Initialize the application
app = create_app()
manager = Manager(app)

# Add database migration commands
manager.add_command('db', MigrateCommand)

# Custom development server with auto-reload
manager.add_command("runserver", Server(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),
    use_debugger=True,
    use_reloader=True
))

@manager.command
def init_db():
    """Initialize the database with default data"""
    from app.models import AIAgent
    
    # Create tables
    db.create_all()
    
    # Seed initial AI agents
    agents = [
        {
            "id": "content_creator_v2",
            "name": "Content Creator Pro",
            "description": "Generates HD marketing content",
            "version": "2.4.1",
            "endpoint": "/api/agents/content"
        },
        {
            "id": "social_poster_v3",
            "name": "Social Media Manager",
            "description": "Automates posting across 10+ platforms",
            "version": "3.1.0",
            "endpoint": "/api/agents/social"
        }
    ]
    
    for agent_data in agents:
        if not AIAgent.query.get(agent_data['id']):
            agent = AIAgent(**agent_data)
            db.session.add(agent)
    
    db.session.commit()
    print("Database initialized with seed data")

@manager.command
def start_agents():
    """Launch all AI agents in background threads"""
    agents = [
        ContentCreatorAgent(),
        SocialPosterAgent(),
        ClientSupportAgent(),
        PaymentProcessorAgent()
    ]
    
    def run_agent(agent):
        print(f"Starting {agent.agent_id}...")
        try:
            # In production, this would connect to message queue
            while True:
                agent.process_next_task()
        except KeyboardInterrupt:
            print(f"Stopping {agent.agent_id}")
    
    threads = []
    for agent in agents:
        t = threading.Thread(target=run_agent, args=(agent,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Keep main thread alive
    for t in threads:
        t.join()

@manager.command
def deploy_afrihost():
    """Deployment script for AfriHost Silver package"""
    commands = [
        "flask db upgrade",
        "python manage.py init_db",
        "gunicorn --bind 0.0.0.0:8000 --workers 4 'app:create_app()'",
        "python manage.py start_agents"
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd.split(), check=True)
            print(f"Success: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Failed: {cmd} - {str(e)}")
            raise

@manager.command
def check_services():
    """Verify all required services are running"""
    services = {
        "MySQL": "mysqladmin ping",
        "Redis": "redis-cli ping",
        "Stripe": "curl -s https://api.stripe.com/v1/ -I | grep HTTP"
    }
    
    all_ok = True
    for name, cmd in services.items():
        try:
            subprocess.run(cmd.split(), check=True, 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ {name} is operational")
        except subprocess.CalledProcessError:
            print(f"❌ {name} service failed")
            all_ok = False
    
    if not all_ok:
        raise SystemExit("Some services are not available")

if __name__ == '__main__':
    manager.run()
