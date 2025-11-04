#!/bin/bash

# Food MCP Server - Docker Management Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
PROD_COMPOSE_FILE="docker-compose.prod.yml"
PROJECT_NAME="food-mcp"

# Functions
print_usage() {
    echo "Usage: $0 {dev|prod|stop|clean|logs|health|rebuild}"
    echo ""
    echo "Commands:"
    echo "  dev      - Start development environment"
    echo "  prod     - Start production environment"
    echo "  stop     - Stop all services"
    echo "  clean    - Stop and remove all containers, volumes, and images"
    echo "  logs     - Show logs from all services"
    echo "  health   - Check health status of services"
    echo "  rebuild  - Rebuild and restart services"
    echo ""
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
}

start_dev() {
    print_info "Starting development environment..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_error "No .env file found. Please create one with your MongoDB Atlas connection string."
        print_info "Example .env file:"
        echo "MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/database"
        exit 1
    fi
    
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
    print_info "Development environment started!"
    print_info "Services available at:"
    echo "  - MCP Server: http://localhost:8000"
    echo "  - Using MongoDB Atlas (from .env file)"
}

start_prod() {
    print_info "Starting production environment..."
    
    # Check if .env.prod exists
    if [ ! -f ".env.prod" ]; then
        print_warning "No .env.prod file found. Creating template..."
        cat > .env.prod << EOF
# MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/database

# Application settings
LOG_LEVEL=INFO
SERVER_PORT=8000
EOF
        print_error "Please edit .env.prod with your production MongoDB Atlas settings before running again."
        exit 1
    fi
    
    docker-compose -f $PROD_COMPOSE_FILE -p $PROJECT_NAME --env-file .env.prod up -d
    print_info "Production environment started!"
}

stop_services() {
    print_info "Stopping all services..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
    docker-compose -f $PROD_COMPOSE_FILE -p $PROJECT_NAME down 2>/dev/null || true
    print_info "All services stopped!"
}

clean_all() {
    print_warning "This will remove all containers, volumes, and images. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Cleaning up..."
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down -v --rmi all
        docker-compose -f $PROD_COMPOSE_FILE -p $PROJECT_NAME down -v --rmi all 2>/dev/null || true
        docker system prune -f
        print_info "Cleanup completed!"
    else
        print_info "Cleanup cancelled."
    fi
}

show_logs() {
    print_info "Showing logs..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f
}

check_health() {
    print_info "Checking service health..."
    
    # Check if containers are running
    containers=$(docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME ps -q)
    
    if [ -z "$containers" ]; then
        print_warning "No containers are running"
        return
    fi
    
    for container in $containers; do
        name=$(docker inspect --format '{{.Name}}' $container | sed 's/\///')
        status=$(docker inspect --format '{{.State.Health.Status}}' $container 2>/dev/null || echo "no-healthcheck")
        
        if [ "$status" = "healthy" ]; then
            print_info "$name: ${GREEN}HEALTHY${NC}"
        elif [ "$status" = "unhealthy" ]; then
            print_error "$name: ${RED}UNHEALTHY${NC}"
        elif [ "$status" = "starting" ]; then
            print_warning "$name: ${YELLOW}STARTING${NC}"
        else
            print_info "$name: ${YELLOW}NO HEALTHCHECK${NC}"
        fi
    done
}

rebuild_services() {
    print_info "Rebuilding services..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
    print_info "Services rebuilt and restarted!"
}

# Main script
main() {
    check_docker
    
    case "${1:-}" in
        dev)
            start_dev
            ;;
        prod)
            start_prod
            ;;
        stop)
            stop_services
            ;;
        clean)
            clean_all
            ;;
        logs)
            show_logs
            ;;
        health)
            check_health
            ;;
        rebuild)
            rebuild_services
            ;;
        *)
            print_usage
            exit 1
            ;;
    esac
}

main "$@"