# Food MCP Server - Structured Output Architecture

A Model Context Protocol (MCP) server providing comprehensive food hierarchy and nutrition data with structured output using Pydantic schemas.

## 🏗️ Architecture

This server uses the **MCP Python SDK** for maximum control and flexibility, providing structured output through Pydantic schemas that ensure consistent data validation and serialization.

### Key Features

- **Structured Output**: All tool responses use Pydantic schemas for validation and serialization
- **MCP Protocol Compliance**: Full adherence to MCP specification with stdio transport
- **MongoDB Atlas Integration**: Cloud-based data storage for scalability
- **Docker Support**: Containerized deployment with optimized builds
- **Comprehensive Tools**: 11 tools covering food hierarchy and nutrition data

## 🛠️ Available Tools

### Food Hierarchy Tools

1. **get_all_food_hierarchy** - Complete food hierarchy dataset
2. **get_categories** - List all food categories  
3. **get_subcategories** - Subcategories for a category
4. **get_food_items** - Food items in category/subcategory
5. **search_food** - Search food items by keyword
6. **find_food_category** - Find category for specific food
7. **list_all_foods** - All unique food names
8. **food_stats** - Dataset statistics

### Food Nutrition Tools

9. **list_food_names** - Foods with nutrition data
10. **get_food_nutrition** - Complete nutrition info for food
11. **search_food_nutrition** - Search nutrition by keyword

## 📊 Structured Output Schemas

All tools return structured data using Pydantic schemas:

### Food Hierarchy Schemas (`schemas/food_hierarchy.py`)
- `FoodHierarchyResponse` - Complete hierarchy data
- `FoodCategoriesResponse` - Category listings
- `FoodSearchResponse` - Search results with context
- `FoodStats` - Dataset statistics

### Food Nutrition Schemas (`schemas/food_item.py`)
- `FoodNutritionResponse` - Complete nutrition data
- `FoodNutrition` - Detailed nutrition with serving sizes
- `ServingInfo` - Structured serving size information

## 🚀 Quick Start

### Local Development

1. **Set up environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env  # Add your MONGODB_URI
   ```

2. **Test the schemas**:
   ```bash
   python test_server.py
   ```

3. **Run the server**:
   ```bash
   python3 run_server.py
   ```

4. **Test with MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector python3 run_server.py
   ```

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t food-mcp-server .
   ```

2. **Run with environment**:
   ```bash
   docker run -e MONGODB_URI="your_mongodb_uri" food-mcp-server
   ```

3. **Use docker-compose**:
   ```bash
   docker-compose up --build
   ```

## 🔧 Configuration

Set the following environment variables:

- `MONGODB_URI` - MongoDB Atlas connection string (required)
- `PYTHONPATH` - Set to `/app` in container
- `PYTHONUNBUFFERED` - Set to `1` for real-time logging

## 📋 Example Tool Responses

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

## 🔄 Migration from FastMCP

This server replaces the previous FastMCP implementation with several advantages:

1. **Better Control**: Low-level server provides complete control over MCP protocol
2. **Structured Output**: Pydantic schemas ensure consistent response format
3. **Type Safety**: Full type checking and validation
4. **Better Debugging**: Direct access to MCP internals for troubleshooting
5. **Production Ready**: Designed for production deployment scenarios

## 🧪 Testing

Run the test suite to verify everything works:

```bash
python3 test_server.py
```

Tests cover:
- Pydantic schema validation
- JSON schema generation for tool definitions
- Structured data serialization
- Response format consistency

## 📚 Development

### Project Structure
```
├── server.py              # Main MCP server implementation
├── run_server.py           # Entry point script
├── schemas/                # Pydantic response schemas
│   ├── food_hierarchy.py   # Hierarchy tool schemas
│   └── food_item.py        # Nutrition tool schemas
├── services/               # Business logic services
├── utils/                  # Database and utilities
├── test_server.py          # Test suite
├── Dockerfile              # Container configuration
└── docker-compose.yml     # Simple deployment config
```

### Adding New Tools

1. Define Pydantic schema in `schemas/`
2. Add tool definition in `handle_list_tools()`
3. Implement handler in `handle_call_tool()`
4. Return `CallToolResult` with structured content
5. Add tests in `test_server.py`

## 🚀 Production Deployment

The server is production-ready with:

- **Security**: Non-root user in Docker container
- **Logging**: Structured logging with appropriate levels
- **Error Handling**: Comprehensive error responses
- **Health Checks**: Docker health check configuration
- **Resource Management**: Multi-stage Docker builds for smaller images

## 📖 MCP Protocol Compliance

This server fully implements the MCP specification:

- **stdio Transport**: Standard input/output communication
- **Tool Discovery**: Dynamic tool listing with schemas
- **Structured Responses**: Consistent response format
- **Error Handling**: Proper error response structure
- **Lifecycle Management**: Proper initialization and cleanup

## 🤝 Contributing

1. Follow the existing Pydantic schema patterns
2. Add comprehensive tests for new features
3. Ensure Docker builds pass
4. Update documentation for new tools