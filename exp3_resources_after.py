# -*- coding: utf-8 -*-
"""Ресурсы ПОСЛЕ изменения файлов (задание 2)."""
import asyncio, importlib.util, sys

spec = importlib.util.spec_from_file_location("mcp_server", "mcp-server.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["mcp_server"] = mod
spec.loader.exec_module(mod)

from fastmcp import Client

async def main():
    async with Client(mod.server) as client:
        for uri in ("entry-weather-example://weather-letter", "info-excursion://Paris-trips"):
            data = await client.read_resource(uri)
            print(f"[resource после изменения] {uri} ->\n{data[0].text}")

asyncio.run(main())
