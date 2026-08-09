import sys
import json
import urllib.request
import urllib.error
import subprocess

def query_merlin_bridge(prompt):
    url = "http://127.0.0.1:8000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer merlin-local-bridge"
    }
    
    # We formulate a strict prompt for Opus so it acts purely as the Planner
    system_prompt = (
        "You are the Lead Architect in a Commander/Executor swarm. "
        "The user will give you a high-level task. Your job is to break it down into a highly specific, "
        "step-by-step implementation plan. "
        "DO NOT write raw code blocks or attempt to output file edits. "
        "Just write the logical plan. The Executor model will read your plan and write the code."
    )
    
    data = {
        "model": "openai/claude-4.8-opus",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Commander] Error querying Merlin Bridge: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python hybrid_swarm.py 'Your task here'")
        sys.exit(1)
        
    task = sys.argv[1]
    
    print(f"\n[Commander] Querying Merlin (Opus 4.8) for the implementation plan for: '{task}'...\n")
    plan = query_merlin_bridge(task)
    
    if not plan:
        print("[Commander] Failed to get plan. Make sure the Merlin Bridge (server.py) is running on port 8000.")
        sys.exit(1)
        
    print("===================== THE PLAN =====================")
    print(plan)
    print("====================================================")
    
    print("\n[Commander] Handing plan to local Executor (Ollama qwen2.5:3b) via Aider...\n")
    
    # We pass the plan to aider. Aider handles connecting to Ollama natively.
    aider_cmd = [
        "aider", 
        "--model", "ollama/qwen2.5:3b",
        "--message", f"Please execute this implementation plan perfectly:\n\n{plan}"
    ]
    
    # Forward the rest of the arguments to aider (if any)
    aider_cmd.extend(sys.argv[2:])
    
    try:
        subprocess.run(aider_cmd)
    except KeyboardInterrupt:
        print("\n[Commander] Swarm interrupted by user.")
    
if __name__ == "__main__":
    main()
