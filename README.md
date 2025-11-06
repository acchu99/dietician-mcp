# Food MCP Server

## Overview

The Food MCP Server is a Model Context Protocol (MCP) implementation that provides comprehensive food hierarchy and nutrition data through a structured API. Built with the MCP Python SDK and StreamableHTTP transport, the server delivers validated data responses using Pydantic schemas for enterprise-grade data consistency.

## Architecture

The server architecture leverages the MCP Python SDK with StreamableHTTP transport to enable web-based access. All data responses are structured through Pydantic schemas, ensuring consistent validation and serialization across all endpoints.

### Core Features

- **Structured Data Output**: All tool responses utilize Pydantic schemas for data validation and serialization
- **StreamableHTTP Transport**: Web-accessible MCP server implementation
- **MongoDB Atlas Integration**: Cloud-based data storage solution for scalability
- **Container Support**: Docker-based deployment with optimized build configurations
- **Comprehensive Tool Suite**: Eleven distinct tools covering food hierarchy and nutrition data

## Available Tools

### Food Hierarchy Management

1. **get_all_food_hierarchy** - Retrieve complete food hierarchy dataset
2. **get_categories** - List all available food categories
3. **get_subcategories** - Retrieve subcategories for a specified category
4. **get_food_items** - List food items within category or subcategory
5. **search_food** - Search food items using keyword parameters
6. **find_food_category** - Locate category for specific food item
7. **list_all_foods** - Retrieve all unique food names in dataset
8. **food_stats** - Generate comprehensive dataset statistics

### Food Nutrition Analysis

9. **list_food_names** - List foods with available nutrition data
10. **get_food_nutrition** - Retrieve complete nutrition information for specified food
11. **search_food_nutrition** - Search nutrition data using keyword parameters

## Data Structure Schemas

All tools return structured data using Pydantic validation schemas:

### Food Hierarchy Schemas (schemas/food_hierarchy.py)
- `FoodHierarchyResponse` - Complete hierarchy data structure
- `FoodCategoriesResponse` - Category listing responses
- `FoodSearchResponse` - Search results with contextual information
- `FoodStats` - Comprehensive dataset statistics

### Food Nutrition Schemas (schemas/food_item.py)
- `FoodNutritionResponse` - Complete nutrition data structure
- `FoodNutrition` - Detailed nutrition information with serving sizes
- `ServingInfo` - Structured serving size information

## Installation and Setup

### Local Development Environment

1. **Environment Configuration**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env  # Configure your MONGODB_URI
   ```

2. **Schema Validation Testing**:
   ```bash
   python3 test_server.py
   ```

3. **Server Initialization**:
   ```bash
   python3 run_server.py
   # Server will be available at http://localhost:8000
   ```

4. **MCP Inspector Integration**:
   ```bash
   npx @modelcontextprotocol/inspector http://localhost:8000/mcp
   ```

5. **Endpoint Access**:
   - MCP StreamableHTTP endpoint: `http://localhost:8000/mcp`
   - CORS headers are enabled for browser access
   - Server logs provide startup information including listening address

### Container Deployment

1. **Image Build Process**:
   ```bash
   docker build -t food-mcp-server .
   ```

2. **Container Execution**:
   ```bash
   docker run -e MONGODB_URI="your_mongodb_uri" -p 8000:8000 food-mcp-server
   ```

3. **Docker Compose Deployment**:
   ```bash
   docker-compose up --build
   ```

## Configuration Management

Configure the following environment variables:

- `MONGODB_URI` - MongoDB Atlas connection string (required)
- `PYTHONPATH` - Set to `/app` in container environment
- `PYTHONUNBUFFERED` - Set to `1` for real-time logging output

## Response Examples

### Structured Categories Response
```json
{
  "categories": ["Vegetables", "Fruits", "Proteins"],
  "total_count": 3
}
```

### Structured Nutrition Response
```json
{
  "requested_name": "Apple",
  "found": true,
  "nutrition": {
    "name": "Apple",
    "display_portion_calories": 95,
    "display_portion_size": "1 medium",
    "nutrients": {
      "calories": 95,
      "protein_g": 0.5,
      "carbs_g": 25.0,
      "fiber_g": 4.0
    }
  }
}
```

## Migration from FastMCP Implementation

This server implementation replaces the previous FastMCP implementation with several key advantages:

1. **Enhanced Control**: Low-level server implementation provides complete control over MCP protocol implementation
2. **Structured Output**: Pydantic schemas ensure consistent response format across all endpoints
3. **Type Safety**: Comprehensive type checking and validation throughout the application
4. **Improved Debugging**: Direct access to MCP internals for enhanced troubleshooting capabilities
5. **Production Readiness**: Architecture designed specifically for production deployment scenarios

## Testing and Validation

Execute the comprehensive test suite to verify system functionality:

```bash
python3 test_server.py
```

Test coverage includes:
- Pydantic schema validation and serialization
- JSON schema generation for tool definitions
- Structured data serialization processes
- Response format consistency verification

## Development Guide

### Project Structure
```
├── server.py              # Main MCP server implementation
├── run_server.py           # Application entry point script
├── schemas/                # Pydantic response schemas
│   ├── food_hierarchy.py   # Hierarchy tool schemas
│   └── food_item.py        # Nutrition tool schemas
├── services/               # Business logic services
├── utils/                  # Database and utility functions
├── test_server.py          # Comprehensive test suite
├── Dockerfile              # Container configuration
└── docker-compose.yml     # Deployment configuration
```

### Adding New Tools

1. Define Pydantic schema in appropriate `schemas/` module
2. Add tool definition in `handle_list_tools()` method
3. Implement tool handler in `handle_call_tool()` method
4. Return `CallToolResult` with structured content
5. Add corresponding tests in `test_server.py`

## Production Deployment

The server is designed for production environments with the following features:

- **Security**: Non-root user execution in Docker container environment
- **Logging**: Structured logging implementation with appropriate severity levels
- **Error Handling**: Comprehensive error response mechanisms
- **Health Monitoring**: Docker health check configuration for container orchestration
- **Resource Optimization**: Multi-stage Docker builds for minimal image size

## MCP Protocol Compliance

This server fully implements the Model Context Protocol specification:

- **stdio Transport**: Standard input/output communication protocol
- **Tool Discovery**: Dynamic tool listing with comprehensive schemas
- **Structured Responses**: Consistent response format across all endpoints
- **Error Handling**: Standardized error response structure
- **Lifecycle Management**: Proper initialization and cleanup procedures

## Contributing Guidelines

1. Follow established Pydantic schema patterns for data validation
2. Add comprehensive test coverage for new features and functionality
3. Ensure Docker build processes complete successfully
4. Update documentation to reflect new tools and capabilities
````