#!/bin/bash

# Build the frontend
cd frontend
npm install
npm run build

# Configure GitHub Pages
cd dist
echo "yourdomain.co.za" > CNAME

# Deploy to gh-pages branch
git init
git add -A
git commit -m "Deploy $(date +'%Y-%m-%d %H:%M:%S')"
git push -f git@github.com:yourusername/yourrepo.git main:gh-pages
