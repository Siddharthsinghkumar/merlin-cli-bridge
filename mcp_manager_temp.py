import contextlib
import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPManager:
    def __init__(self):
        self.sessions = {}
        self.stack = contextlib.AsyncExitStack()
        self.tools = []

    async def start(self):
        try:
            with open("mcp_servers.json", "r") as f:
                config = json.load(f)
        except Exception as e:
            print(f"MCP config not found or invalid: {e}")
            return

        for name, info in config.get("mcpServers", {}).items():
            cmd = info.get("command")
            args = info.get("args", [])
            env = info.get("env", {})
            params = StdioServerParameters(command=cmd, args=args, env=env)
            
            try:
                stdio_transport = await self.stack.enter_async_context(stdio_client(params))
                read, write = stdio_transport
                session = await self.stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                self.sessions[name] = session
                
                tools_res = await session.list_tools()
                for t in tools_res.tools:
                    self.tools.append({
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.inputSchema,
                        "server": name
                    })
                print(f"Loaded MCP server {name} with tools: {[t.name for t in tools_res.tools]}")
            except Exception as e:
                print(f"Failed to load MCP server {name}: {e}")

    async def call_tool(self, name, arguments):
        for t in self.tools:
            if t["name"] == name:
                session = self.sessions[t["server"]]
                res = await session.call_tool(name, arguments)
                return res
        return {"isError": True, "content": [{"type": "text", "text": f"Tool {name} not found"}]}
        
mcp_manager = MCPManager()
