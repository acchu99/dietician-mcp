# 🐳 Docker Setup for Food MCP Server

This directory contains a complete Docker setup for the Food MCP Server with MongoDB integration.

## 📁 Docker Files Overview

- **`Dockerfile`** - Multi-stage build for optimized production images
- **`docker-compose.yml`** - Development environment with MongoDB and Mongo Express
- **`docker-compose.prod.yml`** - Production environment configuration
- **`.dockerignore`** - Excludes unnecessary files from Docker builds
- **`docker-run.sh`** - Management script for easy Docker operations
- **`scripts/init-mongo.js`** - MongoDB initialization script
- **`nginx/nginx.conf`** - Nginx reverse proxy configuration

## 🚀 Quick Start

### Development Environment

```bash
# Start development environment (includes MongoDB + Mongo Express UI)
./docker-run.sh dev

# View logs
./docker-run.sh logs

# Check service health
./docker-run.sh health

# Stop services
./docker-run.sh stop
```

### Production Environment

```bash
# Create production environment file
cp .env .env.prod
# Edit .env.prod with your production MongoDB URI

# Start production environment
./docker-run.sh prod
```

## 🛠️ Available Services

### Development Environment

| Service | URL | Description |
|---------|-----|-------------|
| MCP Server | `http://localhost:8000` | FastMCP Food Hierarchy Server |
| MongoDB Atlas | `External` | Your cloud MongoDB database |

### Production Environment

| Service | URL | Description |
|---------|-----|-------------|
| MCP Server | `http://localhost:8000` | FastMCP Server (behind Nginx) |
| Nginx | `http://localhost:80` | Reverse proxy with rate limiting |
| MongoDB Atlas | `External` | Your cloud MongoDB database |

## 📋 Management Commands

```bash
# Development
./docker-run.sh dev          # Start dev environment
./docker-run.sh prod         # Start production environment
./docker-run.sh stop         # Stop all services
./docker-run.sh logs         # Show logs
./docker-run.sh health       # Check service health
./docker-run.sh rebuild      # Rebuild and restart
./docker-run.sh clean        # Remove everything (containers, volumes, images)
```

## 🔧 Configuration

### Environment Variables

**Development (.env):**
```bash
# MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority

# Application settings
LOG_LEVEL=INFO
```

**Production (.env.prod):**
```bash
# MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority

# Application settings
LOG_LEVEL=INFO
SERVER_PORT=8000
```

### Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use `.env.example`** as a template for new environments
3. **Rotate MongoDB Atlas credentials** regularly
4. **Use MongoDB Atlas IP whitelist** for additional security
5. **Enable MongoDB Atlas monitoring** and alerts

### Nginx Configuration

Production setup includes:
- **Rate limiting** (10 requests/second)
- **Gzip compression** for JSON responses
- **Health check endpoints**
- **SSL support** (commented out, ready to enable)

## 🏗️ Docker Image Details

### Multi-Stage Build

1. **Builder Stage**: Installs dependencies in virtual environment
2. **Production Stage**: Copies only necessary files for minimal image size

### Security Features

- **Non-root user**: Application runs as `appuser`
- **Minimal base image**: Uses `python:3.11-slim`
- **Health checks**: Built-in container health monitoring
- **Resource limits**: Memory and CPU constraints in production

### Image Optimization

- **Layer caching**: Requirements installed separately for better caching
- **Minimal dependencies**: Only production packages included
- **Clean base**: Removes build tools and caches

## 📊 Monitoring & Health Checks

### Container Health

```bash
# Check all service health
./docker-run.sh health

# View detailed container status
docker-compose -p food-mcp ps

# Check logs for specific service
docker-compose -p food-mcp logs food_mcp_server
```

### MongoDB Atlas Health

```bash
# Check Atlas connection from container
docker exec food_mcp_server python -c "from db import MongoDBClient; import os; print('✅ Connected to Atlas!' if MongoDBClient(os.getenv('MONGODB_URI')).ping() else '❌ Connection failed')"

# Test with MCP tools
docker exec food_mcp_server python -c "from main import food_hierarchy_service; print('Categories:', len(food_hierarchy_service.get_categories()))"
```

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml if 27017/8000/8081 are in use
2. **Memory issues**: Increase Docker memory limits in Docker Desktop
3. **Permission issues**: Ensure docker-run.sh is executable (`chmod +x docker-run.sh`)

### Debug Commands

```bash
# View container logs
docker logs food_mcp_server

# Execute commands in container
docker exec -it food_mcp_server bash

# Check MongoDB connection from app container
docker exec food_mcp_server python -c "from db import MongoDBClient; print('Connected!' if MongoDBClient('mongodb://admin:password123@mongodb:27017/food?authSource=admin').ping() else 'Failed!')"
```

### Log Locations

- **Application logs**: `./logs/` (mounted volume)
- **Nginx logs**: `./logs/nginx/` (if using production setup)
- **MongoDB logs**: Available via `docker logs food_mcp_mongodb`

## 🚢 Deployment

### Local Development

1. Clone repository
2. Run `./docker-run.sh dev`
3. Access services at URLs listed above

### Production Deployment

1. Set up production MongoDB instance
2. Create `.env.prod` with production settings
3. Run `./docker-run.sh prod`
4. Configure SSL certificates in `nginx/ssl/` (optional)
5. Uncomment SSL configuration in `nginx/nginx.conf`

### Cloud Deployment

The Docker setup is cloud-ready for:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **Kubernetes** (add K8s manifests as needed)

## 📈 Performance Tuning

### MongoDB Optimization

- **Indexes**: Automatically created via init script
- **Connection pooling**: Configured in MongoDBClient
- **Memory**: Adjust `--wiredTigerCacheSizeGB` for MongoDB

### Application Optimization

- **Worker processes**: Add Gunicorn for multiple workers
- **Caching**: Add Redis for frequently accessed data
- **Resource limits**: Tune CPU/memory limits in docker-compose.prod.yml

## 🔐 Security Considerations

### Development
- Default credentials are used (change for any external access)
- No SSL/TLS (add for production)

### Production
- Use strong passwords and SSL certificates
- Enable firewall rules
- Regular security updates for base images
- Consider using secrets management (Docker Swarm secrets, Kubernetes secrets)

---

## 📞 Support

For issues with the Docker setup:
1. Check the troubleshooting section above
2. Review logs with `./docker-run.sh logs`
3. Verify service health with `./docker-run.sh health`