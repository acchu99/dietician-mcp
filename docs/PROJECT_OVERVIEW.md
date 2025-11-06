# Food MCP Server - Project Overview

## Project Structure

```
food_mcp/
├── server.py                 # Main HTTP MCP server implementation
├── run_server.py             # Entry point for running the HTTP server
├── test_server.py            # Test suite for schemas and functionality
├── test_http_server.py       # HTTP server configuration test
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container build configuration  
├── docker-compose.yml        # HTTP deployment configuration
├── README.md                 # Comprehensive documentation
├── docs/                     # Documentation files
├── schemas/                  # Pydantic response models
│   ├── food_hierarchy.py     # Food hierarchy tool schemas
│   └── food_item.py          # Nutrition tool schemas
├── services/                 # Business logic layer
│   ├── hierarchy_queries.py  # Food hierarchy operations
│   └── item_service.py       # Food nutrition operations
├── utils/                    # Utilities and database
│   └── db.py                 # MongoDB client
└── logs/                     # Application logs (created at runtime)
```

## Core Components

### Server Implementation
- **server.py** - Main MCP server implementation using the Python SDK
- **run_server.py** - Application entry point with comprehensive error handling
- **test_server.py** - Comprehensive test suite for validation

### Data Models
- **schemas/food_hierarchy.py** - Eight Pydantic models for hierarchy tools
- **schemas/food_item.py** - Three Pydantic models for nutrition tools

### Business Logic
- **services/hierarchy_queries.py** - Food categorization and search operations
- **services/item_service.py** - Nutrition data operations and queries
- **utils/db.py** - MongoDB Atlas connection management

### Deployment
- **Dockerfile** - Multi-stage build configuration for production deployment
- **docker-compose.yml** - Container orchestration configuration
- **requirements.txt** - Complete Python package dependencies

## Architecture Benefits

1. **Clear Separation**: Business logic is properly separated from server implementation
2. **Type Safety**: Pydantic schemas ensure comprehensive data validation
3. **Testing Support**: Isolated components facilitate unit testing
4. **Production Ready**: Docker support with proper error handling mechanisms
5. **MCP Compliant**: Full adherence to protocol specification requirements

## Command Reference

```bash
# Execute test suite
python3 test_server.py

# Test HTTP configuration
python3 test_http_server.py

# Start HTTP server
python3 run_server.py

# Test with MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/sse

# Docker deployment
docker-compose up --build
```

## Available Tools

- **Eight Food Hierarchy Tools** - Categories, search functionality, and statistics
- **Three Food Nutrition Tools** - Nutrition data retrieval and search capabilities
- **Structured Output** - All responses utilize Pydantic validation
- **Error Handling** - Comprehensive error response mechanisms

The project maintains clean architecture, comprehensive organization, and production-ready deployment capabilities.