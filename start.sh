#!/bin/bash

# Zomato MCP Client Startup Script

echo "=================================="
echo "Zomato MCP Client Setup & Startup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "⚠️  No .env file found in backend/"
    echo "Creating .env from .env.example..."
    cp backend/.env.example backend/.env
    echo ""
    echo "📝 Please edit backend/.env and add your ANTHROPIC_API_KEY"
    echo "Then run this script again."
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" backend/.env; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY is not set in backend/.env"
    echo "📝 Please edit backend/.env and add your API key"
    echo "Then run this script again."
    exit 1
fi

echo "✅ Environment configured"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
cd ..
echo "✅ Python dependencies installed"

# Install Node dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..
echo "✅ Node.js dependencies installed"

echo ""
echo "=================================="
echo "🚀 Starting Application..."
echo "=================================="
echo ""

# Start backend in background
echo "Starting FastAPI backend on http://localhost:8000..."
cd backend
source venv/bin/activate
python api.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting React frontend on http://localhost:3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================="
echo "✅ Application is running!"
echo "=================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Handle cleanup
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait
