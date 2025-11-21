#!/bin/bash

# Script to run tests before starting the application
# Exit on any error
set -e

echo "🧪 Running tests (this will start the server first)..."
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test

# Store the exit code
TEST_EXIT_CODE=$?

# Clean up test containers
docker compose -f docker-compose.test.yml down

# Check if tests passed
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "❌ Tests failed! Not deploying application."
    exit $TEST_EXIT_CODE
fi

echo "✅ Tests passed! Building and starting application..."
docker compose up --build -d

echo "🚀 Application is running!"
echo "📊 View logs with: docker compose logs -f"
