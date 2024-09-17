from get_details import get_games_appid, get_game_details
import random
import asyncio
import aiohttp

async def urls(id):
    return f'https://store.steampowered.com/app/{id}/'

async def main():
    names_list = []
    id_list = []
    descriptions = []
    image_urls = []

    steam_id = ("(steam id here)")

    async with aiohttp.ClientSession() as session:
        app_ids = await get_games_appid(session, steam_id)

        if app_ids:
            tasks = [get_game_details(session, app_id) for app_id in app_ids]
            games_details = await asyncio.gather(*tasks)

            for game_details in games_details:
                if game_details:
                    names_list.append(game_details['name'])
                    id_list.append(game_details['id'])
                    descriptions.append(game_details['description'])
                    image_urls.append(game_details['image_url'])
        else:
            print("No games found or failed to retrieve game list.")

    if names_list:
        index = random.randint(0, len(names_list) - 1)
        chosen_name = names_list[index]
        chosen_id = id_list[index]
        chosen_description = descriptions[index]
        chosen_image_url = image_urls[index]

        print(f"Chosen game: {chosen_name}")
        
        url = await urls(chosen_id)

        print(chosen_image_url)
        print(chosen_description)
        print(f"{url}")
    else:
        print("No game names found to display.")

if __name__ == "__main__":
    asyncio.run(main())
