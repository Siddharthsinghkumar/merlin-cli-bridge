#!/bin/bash

# Activate the bridge's virtual environment so we have access to all dependencies
source /home/sidd/project/merlin-cli-bridge/venv/bin/activate

# Check if an argument was provided
if [ $# -eq 0 ]; then
    echo "Usage: ./start_swarm.sh \"Your task here\""
    exit 1
fi

# Run the hybrid swarm orchestrator
python3 /home/sidd/project/merlin-cli-bridge/hybrid_swarm.py "$@"
