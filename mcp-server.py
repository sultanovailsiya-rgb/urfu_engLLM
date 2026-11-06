import asyncio 
import requests
from fastmcp import FastMCP

from src.utils.secrets import is_stdio


server = FastMCP(name='Topic Experiment')


@server.prompt()
def explain_topic(topic : str) -> str:
    "Генерирует промпт для объяснения темы в дружелюбной манере"
    # ИЗМЕНЕНО (эксперимент задания 1): добавлены требование языка и структуры ответа
    return (f"Can you explain {topic} in a beginner friendly manner with simple wordings and no technical jargon. "
            f"Include Concept & Examples. Answer in Russian, structure the answer as: Definition, How it works, Examples.")


@server.resource("entry-weather-example://weather-letter", mime_type="text/markdown")
def write_3way_intro() -> str:
    """Пример написания приветственного сообщения, если пользователь хочет информацию по погоде"""
    with open("src/data/entry_letter.md", "r", encoding="utf-8") as file:
        return file.read()
    
@server.resource("info-excursion://Paris-trips", mime_type="text/markdown")
def write_excursion_intro() -> str:
    """Информация по экскурсиям в Париже"""
    with open("src/data/paris_trips.md", "r", encoding="utf-8") as file:
        return file.read()

@server.resource("info-city://Astrakhan", mime_type="text/markdown")
def write_astrakhan_intro() -> str:
    """Информация о городе Астрахань"""
    with open("src/data/astrakhan.md", "r", encoding="utf-8") as file:
        return file.read()

@server.tool()
async def add(a: int, b: int) -> str:
    """Сумма двух чисел"""
    return str(a + b)


@server.tool()
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Конвертирует температуру между шкалами: c — Цельсий, f — Фаренгейт, k — Кельвин."""
    scales = {"c": "градусов Цельсия", "f": "градусов Фаренгейта", "k": "Кельвинов"}
    if from_unit not in scales or to_unit not in scales:
        wrong = [u for u in (from_unit, to_unit) if u not in scales]
        return f"Неизвестная шкала: {', '.join(wrong)}. Доступны c, f, k."
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15
    if to_unit == "c":
        result = celsius
    elif to_unit == "f":
        result = celsius * 9 / 5 + 32
    else:
        result = celsius + 273.15
    return f"{value} {scales[from_unit]} = {round(result, 2)} {scales[to_unit]}"


@server.tool()
def get_weather(city: str) -> str:
    """
    Получает текущую погоду в городе.
    """

    # 1 Получаем координаты города
    # ИСПРАВЛЕНО (обработка ошибок): таймаут и перехват сетевых сбоев вместо необработанного исключения
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    try:
        geo_resp = requests.get(geo_url, params={"name": city, "count": 1}, timeout=10)
        geo_data = geo_resp.json()
    except requests.RequestException as e:
        return f"Не удалось обратиться к геокодеру ({type(e).__name__}). Попробуйте позже."
    except ValueError:
        return "Геокодер вернул ответ в неверном формате."

    if "results" not in geo_data:
        return "Город не найден."

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    #  Получаем погоду
    weather_url = "https://api.open-meteo.com/v1/forecast"
    try:
        weather_resp = requests.get(
            weather_url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            },
            timeout=10,
        )
        weather_data = weather_resp.json()
    except requests.RequestException as e:
        return f"Не удалось получить погоду из-за ошибки: {type(e).__name__}. Попробуйте позже."
    except ValueError:
        return "Сервис погоды вернул ответ в неверном формате."

    if "current_weather" not in weather_data:
        return "Сервис погоды не вернул данных о погоде."

    temp = weather_data["current_weather"]["temperature"]
    wind = weather_data["current_weather"]["windspeed"]

    return f"Погода в {city}: {temp}°C, ветер {wind} км/ч"


if __name__ == "__main__":
    if is_stdio == 'True':
        # уровен протокола stdio
        server.run(transport="stdio")
    else:
        # уровен протокола streamable-http
        server.run(transport="streamable-http")