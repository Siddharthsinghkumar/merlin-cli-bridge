import asyncio
import aiohttp
import json
import sys
import time
import os

API_BASE = "http://127.0.0.1:8000/v1"

async def test_models():
    print("\n--- Testing GET /v1/models ---")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/models") as resp:
            data = await resp.json()
            if data.get("object") == "list" and len(data.get("data", [])) > 0:
                print("✅ /v1/models returned successfully.")
                print(f"   Found {len(data['data'])} models. First one: {data['data'][0]['id']}")
            else:
                print("❌ /v1/models failed or empty.")
                
async def chat_request(session, messages, stream=False):
    payload = {
        "model": "openai/opus",
        "messages": messages,
        "stream": stream
    }
    async with session.post(f"{API_BASE}/chat/completions", json=payload) as resp:
        if not stream:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            full_text = ""
            async for line in resp.content:
                line = line.decode("utf-8").strip()
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        chunk = json.loads(line[6:])
                        if chunk["choices"][0]["delta"].get("content"):
                            full_text += chunk["choices"][0]["delta"]["content"]
                    except:
                        pass
            return full_text

async def test_context():
    if os.getenv("CI") == "true":
        print("\n--- Skipping Context Memory in CI (Requires Browser) ---")
        return
    print("\n--- Testing Context Memory & Persistent Chat ---")
    async with aiohttp.ClientSession() as session:
        # Turn 1
        msg1 = [{"role": "user", "content": "Remember this secret code: GALAXY-42. Reply only with 'Understood'."}]
        print("User: Remember this secret code: GALAXY-42.")
        ans1 = await chat_request(session, msg1, stream=False)
        print(f"Assistant: {ans1}")
        
        # Turn 2
        msg2 = msg1 + [{"role": "assistant", "content": ans1}, {"role": "user", "content": "What is the capital of France? Reply only with the city name."}]
        print("User: What is the capital of France?")
        ans2 = await chat_request(session, msg2, stream=False)
        print(f"Assistant: {ans2}")
        
        # Turn 3
        msg3 = msg2 + [{"role": "assistant", "content": ans2}, {"role": "user", "content": "What was the secret code I told you to remember earlier? Reply only with the code."}]
        print("User: What was the secret code I told you to remember earlier?")
        ans3 = await chat_request(session, msg3, stream=True) # testing stream at the same time
        print(f"Assistant (streamed): {ans3}")
        
        if "GALAXY-42" in ans3.upper():
            print("✅ Context memory and Tab Pooling successful!")
        else:
            print("❌ Context memory failed!")

async def concurrent_subagent_worker(session, id, query):
    print(f"[Subagent {id}] Starting request...")
    ans = await chat_request(session, [{"role": "user", "content": query}], stream=False)
    print(f"[Subagent {id}] Result: {ans[:60]}...")
    return ans

async def test_concurrent_subagents():
    if os.getenv("CI") == "true":
        print("\n--- Skipping Concurrent Subagents in CI (Requires Browser) ---")
        return
    print("\n--- Testing Concurrent Subagent Tab Pooling ---")
    async with aiohttp.ClientSession() as session:
        tasks = [
            concurrent_subagent_worker(session, 1, "Write a 3 sentence story about a brave knight."),
            concurrent_subagent_worker(session, 2, "Explain quantum physics in 2 sentences.")
        ]
        results = await asyncio.gather(*tasks)
        if len(results) == 2 and len(results[0]) > 0 and len(results[1]) > 0:
             print("✅ Concurrent subagents completed successfully on separate tabs!")
        else:
             print("❌ Concurrent subagents failed!")

async def main():
    await test_models()
    await test_context()
    await test_concurrent_subagents()

if __name__ == "__main__":
    asyncio.run(main())
