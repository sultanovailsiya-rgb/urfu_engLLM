import os
import sys

from langchain_core.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
# ЗАМЕНА модели: вместо ChatOpenAI (для него нужен OPEN_AI_KEY) используется ChatMistralAI,
# langchain-mistralai уже есть в зависимостях проекта
from langchain_mistralai import ChatMistralAI
from loguru import logger

# ИСПРАВЛЕНО (импорт): из корня проекта модуль доступен как src.utils.secrets
from src.utils.secrets import OPEN_AI_KEY

def get_tools_used(response):
    """
    Извлекает информацию об инструментах, использованных в ответе агента.
    """
    tools = []
    for m in response["messages"]:
        if isinstance(m, ToolMessage):
            tools.append({
                "name": m.name,         
                "result": m.content,   
                "tool_call_id": m.tool_call_id 
            })
    return tools

def get_resource_content(resources):
    """
    Извлекает содержимое ресурса с определенным URI из списка ресурсов.
    """
    for blob in resources:
        logger.info(f"URI: {blob.metadata['uri']}, MIME type: {blob.mimetype}")
        if str(blob.metadata['uri']) in "entry-weather-example://weather-letter":
            content = blob.as_string()
            return content
        
def get_all_resources(resources):
    """
    Собирает содержимое всех ресурсов в словарь {uri: текст} для контекста агента.
    """
    collected = {}
    for blob in resources:
        collected[str(blob.metadata['uri'])] = blob.as_string()
    return collected

def client_setup():
    client = MultiServerMCPClient(
        {
            "main": {
                "transport": "stdio", 
                # ИСПРАВЛЕНО (путь к серверу): берётся из текущего проекта, а не захардкоженный C:\documents\...
                "command": sys.executable,
                "args": [os.path.abspath("mcp-server.py")],
                # без IS_STDIO=True сервер уходит в streamable-http, и stdio-клиент не подключится
                "env": {**os.environ, "IS_STDIO": "True"},
            }
        }
    )
    return client

def model_setup():
    # ЗАМЕНЕНА модель: gpt-4o-mini требует OPEN_AI_KEY, которого нет в окружении;
    # ключ задаётся в переменной окружения MISTRAL_API_KEY (или в .env)
    model = ChatMistralAI(
        model="ministral-14b-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY", ""),  # Замените на свой ключ!
        temperature=0.1,
        max_tokens=1000)
    return model