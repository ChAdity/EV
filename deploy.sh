#!/bin/bash

# EV Charging Station Predictor - Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🔋 EV Charging Station Predictor - Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required commands exist
check_requirements() {
    print_status "Checking requirements..."
    
    commands=("python3" "pip" "docker" "docker-compose")
    missing_commands=()
    
    for cmd in "${commands[@]}"; do
        if ! command -v $cmd &> /dev/null; then
            missing_commands+=($cmd)
        fi
    done
    
    if [ ${#missing_commands[@]} -ne 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_status "Please install the missing requirements and try again."
        exit 1
    fi
    
    print_success "All requirements satisfied"
}

# Create necessary directories
setup_directories() {
    print_status "Setting up directories..."
    
    mkdir -p static
    mkdir -p templates
    
    print_success "Directories created"
}

# Function to deploy locally
deploy_local() {
    print_status "Starting local deployment..."
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Check if models exist
    if [ ! -d "evtotal final/models" ]; then
        print_warning "ML models directory not found. Please ensure 'evtotal final/models' exists with trained models."
    fi
    
    # Start the application
    print_status "Starting the application..."
    python app.py &
    APP_PID=$!
    
    # Wait a moment for the app to start
    sleep 5
    
    # Check if the application is running
    if ps -p $APP_PID > /dev/null; then
        print_success "Application started successfully!"
        print_status "Access the dashboard at: http://localhost:8000"
        print_status "API documentation at: http://localhost:8000/docs"
        print_status "Press Ctrl+C to stop the application"
        wait $APP_PID
    else
        print_error "Failed to start the application"
        exit 1
    fi
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Starting Docker deployment..."
    
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t ev-station-predictor .
    
    # Stop and remove existing container
    print_status "Stopping existing container (if any)..."
    docker stop ev-station-predictor 2>/dev/null || true
    docker rm ev-station-predictor 2>/dev/null || true
    
    # Run new container
    print_status "Starting new container..."
    docker run -d \
        --name ev-station-predictor \
        -p 8000:8000 \
        -v "$(pwd)/evtotal final:/app/evtotal final:ro" \
        -v "$(pwd)/static:/app/static" \
        ev-station-predictor
    
    # Wait for container to start
    sleep 10
    
    # Check if container is running
    if docker ps | grep -q ev-station-predictor; then
        print_success "Docker container started successfully!"
        print_status "Access the dashboard at: http://localhost:8000"
        print_status "View logs: docker logs ev-station-predictor"
        print_status "Stop container: docker stop ev-station-predictor"
    else
        print_error "Failed to start Docker container"
        docker logs ev-station-predictor
        exit 1
    fi
}

# Function to deploy with Docker Compose
deploy_compose() {
    print_status "Starting Docker Compose deployment..."
    
    # Stop existing services
    print_status "Stopping existing services..."
    docker-compose down 2>/dev/null || true
    
    # Start services
    print_status "Starting services with Docker Compose..."
    docker-compose up -d --build
    
    # Wait for services to start
    sleep 15
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Docker Compose services started successfully!"
        print_status "Access the dashboard at: http://localhost:8000"
        print_status "View logs: docker-compose logs"
        print_status "Stop services: docker-compose down"
    else
        print_error "Failed to start Docker Compose services"
        docker-compose logs
        exit 1
    fi
}

# Function to run health check
health_check() {
    print_status "Running health check..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8000/api/stats > /dev/null; then
            print_success "Health check passed! Application is running correctly."
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - waiting for application..."
        sleep 2
        ((attempt++))
    done
    
    print_error "Health check failed after $max_attempts attempts"
    return 1
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local     Deploy locally with Python"
    echo "  docker    Deploy with Docker container"
    echo "  compose   Deploy with Docker Compose"
    echo "  check     Run health check only"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local"
    echo "  $0 docker"
    echo "  $0 compose"
}

# Main deployment logic
main() {
    case "${1:-help}" in
        "local")
            check_requirements
            setup_directories
            deploy_local
            ;;
        "docker")
            check_requirements
            setup_directories
            deploy_docker
            health_check
            ;;
        "compose")
            check_requirements
            setup_directories
            deploy_compose
            health_check
            ;;
        "check")
            health_check
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

# Cleanup function
cleanup() {
    print_status "Cleaning up..."
    # Kill background processes if any
    jobs -p | xargs -r kill 2>/dev/null || true
}

# Set trap for cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"