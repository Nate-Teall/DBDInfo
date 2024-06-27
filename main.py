import discord
import os

from apis.dbd import DbdApi
from apis.steam import SteamApi

from commands.command_utils import CommandUtils
from commands.screams import Screams
from commands.escapes import Escapes
from commands.stats import Stats

DBD = DbdApi()
STEAM = SteamApi()
UTILS = CommandUtils()

class MyClient(discord.Client):

    # This shouldn't be hard coded, I will find a way to get the total number of achievements from steam.
    total_achievements = 255

    grade_strings = [
        "Ash IV",
        "Ash III",
        "Ash II",
        "Ash I",
        "Bronze IV",
        "Bronze III",
        "Bronze II",
        "Bronze I",
        "Silver IV",
        "Silver III",
        "Silver II",
        "Silver I",
        "Gold IV",
        "Gold III",
        "Gold II",
        "Gold I",
        "Iridescent IV",
        "Iridescent III",
        "Iridescent II",
        "Iridescent I"
    ]

    commands = {
        "-stats":Stats(DBD, STEAM, UTILS),
        "-screams":Screams(DBD, STEAM),
        "-escapes":Escapes(DBD, STEAM, UTILS)
    }

    async def on_ready(self):
        print(f'Logged on as {self.user}!') 
        # Not sure if this is the best way to handle the utils methods
        UTILS.set_pfp_url(self.user.display_avatar.url)

    async def on_message(self, message):

        if message.content.startswith("-"):
            args = message.content.split()
            arg_count = len(args)
            response = [None, None]

            # Check if the command is valid
            if args[0] not in self.commands:
                response[0] = "Command " + args[0] + " not found!"

            else:
                command = self.commands[args[0]]

                # Check if the proper number of arguments was given
                # Every command must have a field called num_args
                if arg_count < command.num_args:
                    response[0] = f"Missing arguments:\n\tUsage: " + command.usage

                else:
                    # Every command must have a run function that takes an array of arguments
                    # and returns a array that contains [message text, embed], one can be None
                    response = command.run(args)
            
            await message.channel.send(content=response[0], embed=response[1])

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))