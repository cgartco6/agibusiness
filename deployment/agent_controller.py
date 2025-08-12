import subprocess
import psutil
from datetime import datetime

class AGIController:
    def __init__(self):
        self.workers = {
            'content_creator': 0,
            'social_poster': 0,
            'client_support': 0
        }
    
    def spawn_worker(self, agent_type):
        """Autonomously deploys new AI agents"""
        cmd = f"python {agent_type}_worker.py --daemon"
        subprocess.Popen(cmd.split())
        self.workers[agent_type] += 1
        self.log_activity(f"Spawned {agent_type} worker")
    
    def heal_system(self):
        """Self-repair function"""
        for proc in psutil.process_iter():
            if 'agi_worker' in proc.name() and proc.status() == 'zombie':
                proc.kill()
                self.spawn_worker(proc.name().split('_')[0])
        
        self.log_activity("System self-healing completed")

    def log_activity(self, message):
        with open('/var/log/agi_operations.log', 'a') as f:
            f.write(f"{datetime.now()} | {message}\n")

# Main autonomous loop
if __name__ == "__main__":
    controller = AGIController()
    while True:
        controller.heal_system()
        time.sleep(300)  # Check every 5 minutes
