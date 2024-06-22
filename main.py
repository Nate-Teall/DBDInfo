import discord
import os
from dbd import DbdApi

DBD = DbdApi()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!') 

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if message.content.startswith("-"):
            params = message.content.split()

            match params[0]:
                case "-screams": 
                    try:
                        scream_count = DBD.get_player_screams(params[0])
                        await message.channel.send("Yikes! You've screamed", scream_count, "times!")

                    except ValueError:
                        await message.channel.send("Player", params[0], "not found!")
                    
                case _: 
                    return

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))

#if __name__ == "__main__":
#    main()