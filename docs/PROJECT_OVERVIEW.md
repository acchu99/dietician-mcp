# Food MCP Server - Project Overview

## 📁 Project Structure

```
food_mcp/
├── 📄 server.py                 # Main MCP server implementation
├── 🚀 run_server.py             # Entry point for running the server
├── 🧪 test_server.py            # Test suite for schemas and functionality
├── 📋 requirements.txt          # Python dependencies
├── 🐳 Dockerfile                # Container build configuration  
├── 🐳 docker-compose.yml        # Simple deployment configuration
├── 📖 README.md                 # Comprehensive documentation
├── 📄 CONVERSION_SUMMARY.md     # Migration details from FastMCP
├── 📂 schemas/                  # Pydantic response models
│   ├── food_hierarchy.py        # Food hierarchy tool schemas
│   └── food_item.py             # Nutrition tool schemas
├── 📂 services/                 # Business logic layer
│   ├── hierarchy_queries.py     # Food hierarchy operations
│   └── item_service.py          # Food nutrition operations
├── 📂 utils/                    # Utilities and database
│   └── db.py                    # MongoDB client
└── 📂 logs/                     # Application logs (created at runtime)
```

## 🔧 Core Components

### Server Implementation
- **`server.py`** - Main MCP server using the Python SDK
- **`run_server.py`** - Entry point with proper error handling
- **`test_server.py`** - Comprehensive test suite

### Data Models
- **`schemas/food_hierarchy.py`** - 8 Pydantic models for hierarchy tools
- **`schemas/food_item.py`** - 3 Pydantic models for nutrition tools

### Business Logic
- **`services/hierarchy_queries.py`** - Food categorization and search
- **`services/item_service.py`** - Nutrition data operations
- **`utils/db.py`** - MongoDB Atlas connection management

### Deployment
- **`Dockerfile`** - Multi-stage build for production
- **`docker-compose.yml`** - Simple container orchestration
- **`requirements.txt`** - All necessary Python packages

## 🎯 Clean Architecture Benefits

1. **Clear Separation**: Business logic separated from server implementation
2. **Type Safety**: Pydantic schemas ensure data validation
3. **Easy Testing**: Isolated components for unit testing
4. **Production Ready**: Docker support with proper error handling
5. **MCP Compliant**: Full adherence to protocol specification

## 🚀 Quick Commands

```bash
# Run tests
python3 test_server.py

# Start server
python3 run_server.py

# Test with MCP Inspector
npx @modelcontextprotocol/inspector python3 run_server.py

# Docker deployment
docker-compose up --build
```

## 📊 Tools Available

- **8 Food Hierarchy Tools** - Categories, search, stats
- **3 Food Nutrition Tools** - Nutrition data and search
- **Structured Output** - All responses use Pydantic validation
- **Error Handling** - Comprehensive error responses

The project is now clean, well-organized, and production-ready! 🎉