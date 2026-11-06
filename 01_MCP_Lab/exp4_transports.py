# -*- coding: utf-8 -*-
"""Эксперимент с транспортами (задания 4-5): stdio против streamable-http."""
import asyncio, os, subprocess, sys, time

from fastmcp import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

SERVER = os.path.abspath("mcp-server.py")
HTTP_URL = "http://127.0.0.1:8000/mcp"

async def measure(label, client):
    t0 = time.perf_counter()
    async with client as c:
        await c.list_tools()
        t_connect = time.perf_counter() - t0
        times = []
        for _ in range(5):
            t1 = time.perf_counter()
            await c.call_tool("add", {"a": 2, "b": 3})
            times.append(time.perf_counter() - t1)
        t2 = time.perf_counter()
        await c.get_prompt("explain_topic", {"topic": "Python"})
        await c.read_resource("entry-weather-example://weather-letter")
        t_ctx = time.perf_counter() - t2
        print(f"[{label}] подключение (старт процесса + сессия): {t_connect:.3f} с")
        print(f"[{label}] вызов add x5: среднее {sum(times)/len(times)*1000:.1f} мс, мин {min(times)*1000:.1f} мс, макс {max(times)*1000:.1f} мс")
        print(f"[{label}] get_prompt + read_resource: {t_ctx*1000:.1f} мс")

async def main():
    print("=== stdio: сервер запускается клиентом как дочерний процесс ===")
    env = {**os.environ, "IS_STDIO": "True"}
    tr = StdioTransport(command=sys.executable, args=[SERVER], env=env, cwd=os.getcwd())
    await measure("stdio", Client(tr))

    print("\n=== streamable-http: сервер работает отдельным процессом ===")
    env2 = {**os.environ, "IS_STDIO": "False"}
    proc = subprocess.Popen([sys.executable, SERVER], env=env2, cwd=os.getcwd(),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                import socket
                s = socket.create_connection(("127.0.0.1", 8000), timeout=1)
                s.close()
                break
            except OSError:
                time.sleep(0.5)
        await measure("streamable-http", Client(StreamableHttpTransport(url=HTTP_URL)))
    finally:
        proc.terminate()

asyncio.run(main())
