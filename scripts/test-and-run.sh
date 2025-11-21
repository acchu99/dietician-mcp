#!/bin/bash

# Script to run tests before starting the application
# Exit on any error
set -e

echo "🧪 Running tests (this will start the server first)..."
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test

# Clean up test containers
docker compose -f docker-compose.test.yml down

echo "✅ Tests passed! Building and starting application..."
docker compose --profile production up --build -d

echo "🚀 Application is running!"
echo "📊 View logs with: docker compose --profile production logs -f"
