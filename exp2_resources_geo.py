# -*- coding: utf-8 -*-
"""Анализ регистра (задание 3) и изменение ресурсов (задание 2)."""
import requests

print("=== Геокодинг: регистр и язык названия ===")
for name in ("Paris", "PARIS", "paris", "Москва", "Moscow"):
    r = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": name, "count": 1}, timeout=15).json()
    res = r.get("results") or []
    if res:
        print(f"  {name!r:12} -> широта {res[0]['latitude']}, долгота {res[0]['longitude']}, в базе: {res[0]['name']}")
    else:
        print(f"  {name!r:12} -> не найден")

print("\n=== Ресурсы: содержимое ДО изменения ===")
for path in ("src/data/entry_letter.md", "src/data/paris_trips.md"):
    with open(path, encoding="utf-8") as f:
        print(f"  {path}: {f.read()!r}")
