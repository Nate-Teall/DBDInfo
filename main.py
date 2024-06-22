import discord
import os

from dbd import DbdApi
from steam import SteamApi

DBD = DbdApi()
STEAM = SteamApi()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!') 

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if message.content.startswith("-"):
            params = message.content.split()

            match params[0]:
                # Get a player's total times screamed from their vanity url name. 
                # Not yet sure how to get steam id by username 
                case "-screams": 
                    try:
                        vanity_url = params[1]
                        player_id = STEAM.get_steam_id_64(vanity_url)
                        scream_count = DBD.get_player_screams(player_id)

                        await message.channel.send("Yikes! You've screamed " + str(scream_count) + " times! :scream:")

                    except ValueError:
                        await message.channel.send("Player: " + vanity_url + " not found!")
                    
                case _: 
                    return

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))

#if __name__ == "__main__":
#    main()