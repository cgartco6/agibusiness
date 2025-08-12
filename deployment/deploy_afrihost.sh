#!/bin/bash
# Autonomous deployment to AfriHost Silver Package
rsync -avz --delete \
    --exclude='*.tmp' \
    -e "ssh -i ~/.ssh/afrihost_key" \
    ./afrihost/ user@afrihost-server:/var/www/agibusiness/

# Database migration
ssh -i ~/.ssh/afrihost_key user@afrihost-server <<EOF
cd /var/www/agibusiness
python manage.py migrate
systemctl restart agi-workers
EOF
