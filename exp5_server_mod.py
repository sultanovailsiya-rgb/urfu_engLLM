# -*- coding: utf-8 -*-
"""Проверка модификаций сервера (задание 6): новый tool, новый resource, обработка ошибок."""
import asyncio, importlib.util, sys

spec = importlib.util.spec_from_file_location("mcp_server", "mcp-server.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["mcp_server"] = mod
spec.loader.exec_module(mod)

from fastmcp import Client

async def main():
    async with Client(mod.server) as client:
        tools = await client.list_tools()
        print("tools после модификации:", [t.name for t in tools])
        res = await client.list_resources()
        print("resources после модификации:", [str(r.uri) for r in res])

        print("\n=== Новый tool: convert_temperature ===")
        for args in ({"value": 100, "from_unit": "c", "to_unit": "f"},
                     {"value": 32, "from_unit": "f", "to_unit": "c"},
                     {"value": 300, "from_unit": "k", "to_unit": "c"},
                     {"value": -40, "from_unit": "c", "to_unit": "f"},
                     {"value": 10, "from_unit": "x", "to_unit": "c"}):
            r = await client.call_tool("convert_temperature", args)
            print(f"  {args} -> {r.content[0].text}")

        print("\n=== Новый resource: info-city://Astrakhan ===")
        data = await client.read_resource("info-city://Astrakhan")
        print(data[0].text)

        print("=== Обработка ошибок get_weather ===")
        for city in ("Paris", "PARIS", "paris", "Москва", "Astrakhan", "НесуществующийГород-777"):
            r = await client.call_tool("get_weather", {"city": city})
            print(f"  {city!r:10} -> is_error={r.is_error}: {r.content[0].text}")

asyncio.run(main())
