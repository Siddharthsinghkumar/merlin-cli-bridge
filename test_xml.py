from server import mcp_manager, skill_manager
import asyncio
async def main():
    await mcp_manager.start()
    skill_manager.load_skills()
    t = mcp_manager.get_tools_xml()
    s = skill_manager.get_skills_xml()
    print("MCP len:", len(t))
    print("Skills len:", len(s))
asyncio.run(main())
