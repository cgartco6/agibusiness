#!/bin/bash
# Automated GitHub Pages Deployment Script
# For AGI Business Platform - South African Market

set -e # Exit on error

# Configuration
GH_REPO="yourusername/agi-business-platform"
GH_BRANCH="gh-pages"
TARGET_DIR="frontend"
DOMAIN="www.yourdomain.co.za"

echo "🚀 Starting GitHub Pages Deployment"

# 1. Build the frontend
echo "🔨 Building frontend..."
cd $TARGET_DIR
npm install
npm run build

# 2. Prepare deployment directory
echo "📁 Preparing deployment..."
rm -rf .git/ # Remove any existing git history
cp ../deployment/CNAME ./dist/ # Add custom domain

# 3. Deploy to GitHub Pages
echo "📤 Deploying to GitHub..."
cd dist
git init
git checkout -b $GH_BRANCH
git add -A
git commit -m "Automated deployment $(date +'%Y-%m-%d %H:%M:%S')"

git push -f "https://${GH_TOKEN}@github.com/${GH_REPO}.git" $GH_BRANCH

echo "✅ Successfully deployed to https://$DOMAIN"
