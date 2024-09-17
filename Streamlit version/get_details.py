import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("STEAM_API")
steam_api = KEY

async def get_games_appid(session, steam_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={steam_api}&steamid={steam_id}&format=json"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

            if "response" in data and "games" in data["response"]:
                games = data["response"]["games"]
                return [game["appid"] for game in games]
            else:
                print("Failed to retrieve the game library.")
                return []
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return []

async def get_game_details(session, app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

            if str(app_id) in data and data[str(app_id)].get("success"):
                game_data = data[str(app_id)]["data"]
                return {
                    "name": game_data.get("name", "Unknown Name"),
                    "id": app_id,
                    'description': game_data.get('short_description', ''),
                    'image_url': game_data.get('header_image', ''),
                }
            else:
                print(f"Game details not found for App ID {app_id} or API response error")
                return None
    except aiohttp.ClientError as e:
        print(f"Request failed for App ID {app_id}: {e}")
        return None
