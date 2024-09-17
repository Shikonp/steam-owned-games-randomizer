from steam_integ_async import get_games_appid, get_game_details
import random
import asyncio
import aiohttp
import streamlit as st

async def urls(id):
    return f'https://store.steampowered.com/app/{id}/'

async def main():
    names_list = []
    id_list = []
    descriptions = []
    image_urls = []

    st.write("Steam ID:")
    steam_id = st.text_area("Put your steam id here", value='', height=None)
    if st.button("Suprise me!"):
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
                st.write("No games found or failed to retrieve game list.")

        if names_list:
            index = random.randint(0, len(names_list) - 1)
            chosen_name = names_list[index]
            chosen_id = id_list[index]
            chosen_description = descriptions[index]
            chosen_image_url = image_urls[index]

            st.write(f"Chosen game: {chosen_name}")
            
            url = await urls(chosen_id)

            st.image(chosen_image_url, caption=chosen_name)
            st.write(chosen_description)
            st.markdown(f"{url}")
        else:
            st.write("No game names found to display.")

if __name__ == "__main__":
    asyncio.run(main())
