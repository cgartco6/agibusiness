#!/bin/bash

# 1. Deploy frontend to GitHub Pages
echo "🚀 Deploying to GitHub Pages..."
cd frontend
git init
git add .
git commit -m "Autonomous deployment $(date +%Y%m%d)"
git push origin main --force

# 2. Deploy backend to AfriHost
echo "⚡ Deploying to AfriHost..."
cd ../deployment
chmod +x deploy_afrihost.sh
./deploy_afrihost.sh

# 3. Launch AI ecosystem
echo "🤖 Activating AGI Agents..."
python agent_controller.py --daemon &

echo "✅ System Online at https://agibusiness.co.za"
