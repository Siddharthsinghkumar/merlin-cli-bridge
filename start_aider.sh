#!/bin/bash

# 1. Activate the virtual environment
source /home/sidd/project/merlin-cli-bridge/venv/bin/activate

# 2. Start the API bridge server in the background
echo "Starting Merlin API Bridge on port 8000..."
cd /home/sidd/project/merlin-cli-bridge
xvfb-run -a -s "-screen 0 1920x1080x24" uvicorn server:app --host 127.0.0.1 --port 8000 > server.log 2>&1 &
SERVER_PID=$!

# Trap EXIT to kill the server when this script ends
trap 'echo "Shutting down Merlin API Bridge..."; kill $SERVER_PID 2>/dev/null' EXIT

# Wait a moment for it to start
sleep 3

# 3. Set up OpenAI environment variables
export OPENAI_API_BASE="http://127.0.0.1:8000/v1"
export OPENAI_API_KEY="merlin-local-bridge"

# 4. Start Aider
echo "Starting Aider..."
aider --model openai/claude-4.8-opus --edit-format udiff --no-show-model-warnings "$@"
