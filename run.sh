#!/bin/bash

# Commands with correct paths
backend_cmd="uv run fastapi dev src/main.py"
frontend_cmd="npm run dev"

# Function to start backend
start_backend() {
    echo "Starting backend..."
    (cd api && $backend_cmd) &
    backend_pid=$!
}

# Function to start frontend
start_frontend() {
    echo "Starting frontend..."
    (cd frontend && $frontend_cmd) &
    frontend_pid=$!
}

# Start both processes
start_backend
start_frontend

# Trap Ctrl+C to kill both processes gracefully
trap "echo 'Stopping both processes...'; kill $backend_pid $frontend_pid; exit" SIGINT SIGTERM

# Monitoring loop to restart if a process exits
while true; do
    if ! kill -0 $backend_pid 2>/dev/null; then
        echo "Backend crashed! Restarting..."
        start_backend
    fi

    if ! kill -0 $frontend_pid 2>/dev/null; then
        echo "Frontend crashed! Restarting..."
        start_frontend
    fi

    sleep 2  # Prevent excessive CPU usage
done
