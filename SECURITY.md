# 🔐 MongoDB Atlas Security Guide

## Overview

Your MCP server now uses MongoDB Atlas cloud database instead of a local container, providing better security, scalability, and reliability.

## 🛡️ Security Best Practices

### 1. Environment File Security

```bash
# ✅ DO: Use separate env files for different environments
.env              # Development (never commit!)
.env.prod         # Production (never commit!)
.env.example      # Template (safe to commit)

# ❌ DON'T: Commit sensitive files
git add .env      # NEVER DO THIS
```

### 2. MongoDB Atlas Security

**Connection String Format:**
```bash
mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
```

**Atlas Security Checklist:**
- ✅ Enable **IP Access List** (whitelist your server IPs)
- ✅ Use **strong passwords** (mix of letters, numbers, symbols)
- ✅ Enable **MongoDB Atlas monitoring** and alerts
- ✅ Set up **backup schedules** in Atlas
- ✅ Use **read-only users** for analytics if needed
- ✅ Enable **audit logging** in Atlas (paid tiers)
- ✅ Regularly **rotate credentials**

### 3. Docker Security

**Environment Variable Handling:**
```bash
# ✅ Good: Use env_file in docker-compose
env_file:
  - .env

# ✅ Good: Pass via environment
environment:
  - MONGODB_URI=${MONGODB_URI}

# ❌ Bad: Hardcode in compose file
environment:
  - MONGODB_URI=mongodb+srv://user:pass@cluster...
```

**Container Security:**
- ✅ Runs as **non-root user** (`appuser`)
- ✅ Uses **minimal base image** (python:3.11-slim)
- ✅ **No sensitive files** in image layers
- ✅ **Health checks** for monitoring

### 4. Network Security

**Atlas Network Security:**
- ✅ **VPC Peering** (recommended for production)
- ✅ **Private endpoints** for enterprise
- ✅ **IP allowlisting** instead of 0.0.0.0/0

**Docker Network:**
- ✅ **Isolated Docker network** for containers
- ✅ **No unnecessary port exposure**
- ✅ **Nginx reverse proxy** for production

## 🔧 Setup Instructions

### Development Setup

1. **Create `.env` file:**
```bash
cp .env.example .env
# Edit .env with your Atlas connection string
```

2. **Start development:**
```bash
./docker-run.sh dev
```

### Production Setup

1. **Create production env:**
```bash
cp .env.example .env.prod
# Edit .env.prod with production Atlas settings
```

2. **Deploy:**
```bash
./docker-run.sh prod
```

## 📊 Monitoring Atlas Connection

### Health Checks

```bash
# Test Atlas connection
docker exec food_mcp_server python -c "
from main import food_hierarchy_service; 
print('✅ Connected! Categories:', len(food_hierarchy_service.get_categories()))
"

# Check container health
./docker-run.sh health
```

### Atlas Monitoring

**In MongoDB Atlas Dashboard:**
- Monitor **connection counts**
- Track **query performance** 
- Set up **custom alerts**
- Review **slow query logs**

## 🚨 Incident Response

### Connection Issues

1. **Check Atlas status:** https://status.mongodb.com
2. **Verify IP allowlist** in Atlas
3. **Test credentials** locally
4. **Check container logs:** `docker logs food_mcp_server`

### Security Incidents

1. **Rotate credentials** immediately in Atlas
2. **Update `.env` files** on all servers
3. **Restart containers** with new credentials
4. **Review Atlas audit logs**

## 📝 Environment File Templates

### `.env.example` (Safe to commit)
```bash
# MongoDB Atlas Connection
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority

# Application Settings
LOG_LEVEL=INFO
```

### `.env` (NEVER commit)
```bash
# Your actual development Atlas connection
MONGODB_URI=mongodb+srv://dev_user:dev_password@dev-cluster.mongodb.net/food_dev?retryWrites=true&w=majority
LOG_LEVEL=DEBUG
```

### `.env.prod` (NEVER commit)
```bash
# Your production Atlas connection
MONGODB_URI=mongodb+srv://prod_user:strong_prod_password@prod-cluster.mongodb.net/food_prod?retryWrites=true&w=majority
LOG_LEVEL=INFO
SERVER_PORT=8000
```

## 🎯 Quick Security Audit

```bash
# Check for exposed secrets
grep -r "mongodb" . --exclude-dir=.git --exclude="*.example"

# Verify .env files are gitignored
git check-ignore .env .env.prod

# Check Atlas IP allowlist
# (Do this in Atlas dashboard)

# Test connection with minimal permissions
docker exec food_mcp_server python -c "
import os
from db import MongoDBClient
try:
    client = MongoDBClient(os.getenv('MONGODB_URI'))
    # Test basic read operation
    from main import food_hierarchy_service
    categories = food_hierarchy_service.get_categories()
    print(f'✅ Atlas connection working: {len(categories)} categories')
except Exception as e:
    print(f'❌ Atlas connection failed: {e}')
"
```

---

🔐 **Remember:** Security is an ongoing process. Regularly review and update your security practices!