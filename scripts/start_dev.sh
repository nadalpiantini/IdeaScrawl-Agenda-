#!/bin/bash
# Development startup script for IdeaScrawl Agenda

echo "🚀 Starting IdeaScrawl Agenda Development Environment"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn requests python-dotenv supabase

# Check .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "✏️  Please edit .env with your API keys before continuing"
fi

# Start API server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📊 API docs available at http://localhost:8000/docs"
echo "🔍 Health check: curl http://localhost:8000/health"
echo ""
echo "💡 Next steps:"
echo "   1. Install Chrome extension from /extension folder"
echo "   2. Visit chat.openai.com and start chatting"
echo "   3. Click extension icon to see captured ideas"
echo ""

uvicorn api.generate_page:app --reload --port 8000