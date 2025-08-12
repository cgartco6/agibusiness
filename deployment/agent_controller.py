import subprocess
import psutil
import time
from datetime import datetime
import logging
import requests

class AGIOrchestrator:
    def __init__(self):
        self.agent_config = {
            'content_creator': {
                'min_workers': 2,
                'max_workers': 5,
                'current': 0
            },
            'social_poster': {
                'min_workers': 1,
                'max_workers': 3,
                'current': 0
            }
        }
        logging.basicConfig(filename='agi.log', level=logging.INFO)

    def health_check(self):
        """Autonomous system monitoring"""
        for agent in self.agent_config:
            try:
                resp = requests.get(f'http://localhost:8000/{agent}/status')
                if resp.status_code != 200:
                    self.restart_agent(agent)
            except Exception as e:
                self.redeploy_agent(agent)

    def scale_agents(self):
        """Dynamic resource allocation"""
        current_load = psutil.cpu_percent()
        if current_load > 70:
            self.reduce_workers()
        elif current_load < 30:
            self.add_workers()

    def redeploy_agent(self, agent_type):
        """Complete agent rebuild"""
        subprocess.run(['pkill', '-f', f'{agent_type}_worker'])
        subprocess.Popen(['python3', f'agents/{agent_type}_worker.py'])
        logging.info(f'Redeployed {agent_type} at {datetime.now()}')

if __name__ == "__main__":
    orchestrator = AGIOrchestrator()
    while True:
        orchestrator.health_check()
        orchestrator.scale_agents()
        time.sleep(300)
