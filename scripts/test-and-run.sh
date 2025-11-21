#!/bin/bash

# Script to run tests before starting the application
# Exit on any error
set -e

echo "[INFO] Running tests (this will start the server first)..."
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test

# Store the exit code
TEST_EXIT_CODE=$?

# Clean up test containers
docker compose -f docker-compose.test.yml down

# Check if tests passed
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "[ERROR] Tests failed! Not deploying application."
    exit $TEST_EXIT_CODE
fi

echo "[SUCCESS] Tests passed! Building and starting application..."
docker compose up --build -d

echo "[INFO] Application is running!"
echo "[INFO] View logs with: docker compose logs -f"
