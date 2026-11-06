# -*- coding: utf-8 -*-
"""Задание 1: как изменение текста prompt меняет ответ модели."""
from src.process import model_setup

model = model_setup()

# текст prompt ДО изменения (исходная версия explain_topic)
before = ("Can you explain Python in a beginner friendly manner with simple wordings and no technical jargon. "
          "Include Concept & Examples.")
# текст prompt ПОСЛЕ изменения (текущая версия explain_topic в mcp-server.py)
after = ("Can you explain Python in a beginner friendly manner with simple wordings and no technical jargon. "
         "Include Concept & Examples. Answer in Russian, structure the answer as: Definition, How it works, Examples.")

for label, prompt in (("ДО изменения prompt", before), ("ПОСЛЕ изменения prompt", after)):
    answer = model.invoke(prompt).content
    print(f"=== {label} ===")
    print("текст prompt:", prompt)
    print("ответ модели:", answer)
    print()
