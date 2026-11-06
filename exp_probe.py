# -*- coding: utf-8 -*-
import asyncio, importlib.util, sys

spec = importlib.util.spec_from_file_location("mcp_server", "mcp-server.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["mcp_server"] = mod
spec.loader.exec_module(mod)
print("сервер загружен:", mod.server.name)

from fastmcp import Client

async def main():
    async with Client(mod.server) as client:
        tools = await client.list_tools()
        print("tools:", [(t.name, list(t.inputSchema.get('properties', {}).keys())) for t in tools])
        res = await client.list_resources()
        print("resources:", [str(r.uri) for r in res])
        prompts = await client.list_prompts()
        print("prompts:", [p.name for p in prompts])
        p = await client.get_prompt("explain_topic", {"topic": "Python"})
        print("prompt type:", type(p).__name__)
        print("prompt:", p.messages[0].content.text if hasattr(p.messages[0].content, 'text') else p.messages[0].content)
        r = await client.read_resource("entry-weather-example://weather-letter")
        print("resource read type:", type(r).__name__, "| len:", len(r))
        print("resource[0]:", type(r[0]).__name__, getattr(r[0], 'text', r[0])[:80])

asyncio.run(main())
