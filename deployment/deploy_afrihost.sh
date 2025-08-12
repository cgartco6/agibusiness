#!/bin/bash
# AfriHost Silver Package Deployment Script

SERVER="username@afrihost.server"
SSH_KEY="$HOME/.ssh/afrihost_deploy_key"
APP_DIR="/var/www/agibusiness"
DB_NAME="agi_business_db"

echo "🚀 Starting Autonomous Deployment..."

# 1. Transfer files
rsync -avz -e "ssh -i $SSH_KEY" \
    --exclude={'*.tmp','*.log'} \
    --delete \
    ./backend/ $SERVER:$APP_DIR/

# 2. Database setup
ssh -i $SSH_KEY $SERVER <<EOF
cd $APP_DIR
source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p"\$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME"
python manage.py migrate
sudo systemctl restart gunicorn
EOF

echo "✅ Deployment Complete. AGI System Active."
