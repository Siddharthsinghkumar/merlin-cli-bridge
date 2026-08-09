import concurrent.futures
from openai import OpenAI
import time

# Point the OpenAI client to our local Merlin FastAPI bridge
client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="merlin-local-bridge-key" # Dummy key since our server doesn't check it
)

def run_agent_task(agent_id, prompt):
    print(f"[Agent {agent_id}] Starting workload: '{prompt}'")
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model="opus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        elapsed = time.time() - start_time
        answer = response.choices[0].message.content.strip()
        print(f"\n[Agent {agent_id}] SUCCESS in {elapsed:.1f}s")
        print(f"[Agent {agent_id}] Answer: {answer[:200]}...\n")
        return True
    except Exception as e:
        print(f"\n[Agent {agent_id}] ERROR: {e}")
        return False

def main():
    print("==================================================")
    print("   Starting Agentic Swarm Workload Test (3 Agents)")
    print("==================================================")
    
    # 3 simultaneous agentic workloads
    workloads = [
        "Explain quantum entanglement in exactly one sentence.",
        "Write a 4-line poem about artificial intelligence.",
        "What is the capital of Japan? Just say the name."
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(run_agent_task, i+1, prompt) 
            for i, prompt in enumerate(workloads)
        ]
        
        concurrent.futures.wait(futures)
        
    print("==================================================")
    print("   Agentic Swarm Workload Complete!")
    print("==================================================")

if __name__ == "__main__":
    main()
