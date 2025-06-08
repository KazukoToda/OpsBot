#!/bin/bash

# OpsBot startup script

echo "🤖 Starting OpsBot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Please copy .env.example to .env and add your OpenAI API key."
    if [ -f .env.example ]; then
        echo "💡 Run: cp .env.example .env"
        echo "💡 Then edit .env to add your OPENAI_API_KEY"
    fi
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ] && [ ! -f .env ]; then
    echo "❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable or create .env file."
    exit 1
fi

# Install dependencies if they don't exist
echo "📦 Checking dependencies..."
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "🚀 Starting Streamlit application..."
streamlit run app.py