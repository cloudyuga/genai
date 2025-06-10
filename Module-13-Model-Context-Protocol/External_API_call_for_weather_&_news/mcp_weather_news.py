import os
from typing import Any
import httpx
import urllib.parse
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()
# Initialize FastMCP server
mcp = FastMCP("news_weather")

# Your API keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@mcp.tool()
def fetch_and_review_weather(city: str) -> str:
    """Fetch current weather for a city using OpenWeatherMap."""
    city = city.strip()
    encoded_city = urllib.parse.quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = httpx.get(url)
        response.raise_for_status()
        weather_data = response.json()

        weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        return (
            f"City: {city}\n"
            f"Weather: {weather} ({description})\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
    except Exception as e:
        return f"Error fetching weather: {e}"


@mcp.tool()
def fetch_and_summarize_news(arg: str = None) -> str:
    """Fetch latest BBC News headlines and descriptions."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={NEWS_API_KEY.strip()}"
        response = httpx.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        if not articles:
            return "No news articles found."

        sanitized_articles = []
        for article in articles[:5]:  # limit to top 5
            title = (article.get('title') or '').replace('\n', ' ').strip()
            description = (article.get('description') or '').replace('\n', ' ').strip()
            sanitized_articles.append(f"📰 {title}\n📄 {description}")

        return "\n\n---\n\n".join(sanitized_articles)

    except Exception as e:
        return f"Error fetching news: {e}"

if __name__ == "__main__":
    mcp.run(transport="sse")
