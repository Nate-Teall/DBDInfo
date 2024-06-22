import discord
import os
from dbd import DbdApi

DBD = None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!') 
        DBD = DbdApi()

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content.startswith("-hello"):
            await message.channel.send("sup")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))

#if __name__ == "__main__":
#    main()