#!/bin/bash

# EOTSS Hosting Recommendation System - Production Deployment Script
set -e

echo "🚀 Starting EOTSS Hosting System Production Deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy env.example to .env and configure your environment variables."
    exit 1
fi

# Load environment variables
source .env

# Check required environment variables
required_vars=("SECRET_KEY" "MAIL_USERNAME" "MAIL_PASSWORD" "EOTSS_EMAIL")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var is not set in .env file"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Check if SSL certificates exist
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    echo "⚠️  Warning: SSL certificates not found in ssl/ directory"
    echo "For production, you should obtain proper SSL certificates."
    echo "For testing, you can generate self-signed certificates:"
    echo "  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/key.pem -out ssl/cert.pem"
    read -p "Continue without SSL? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for containers to be healthy
echo "⏳ Waiting for application to be ready..."
sleep 10

# Check if application is responding
echo "🔍 Checking application health..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Application is healthy and responding"
else
    echo "❌ Application health check failed"
    echo "Checking container logs..."
    docker-compose -f docker-compose.prod.yml logs app
    exit 1
fi

# Display deployment information
echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Information:"
echo "  • Application URL: https://$(hostname -I | awk '{print $1}')"
echo "  • Dashboard: https://$(hostname -I | awk '{print $1}')/dashboard"
echo "  • Health Check: https://$(hostname -I | awk '{print $1}')/health"
echo ""
echo "🔧 Useful Commands:"
echo "  • View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  • Stop application: docker-compose -f docker-compose.prod.yml down"
echo "  • Restart application: docker-compose -f docker-compose.prod.yml restart"
echo ""
echo "📧 Email Configuration:"
echo "  • EOTSS Email: $EOTSS_EMAIL"
echo "  • Mail Server: $MAIL_SERVER:$MAIL_PORT"
echo ""
echo "🔒 Security Notes:"
echo "  • Ensure SSL certificates are properly configured"
echo "  • Change default SECRET_KEY in production"
echo "  • Configure firewall rules appropriately"
echo "  • Set up regular backups of assessment_data volume" 