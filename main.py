import discord
import os

from apis.dbd import DbdApi
from apis.steam import SteamApi

from commands.command_utils import CommandUtils
from commands.screams import Screams
from commands.escapes import Escapes
from commands.stats import Stats
from commands.randomize import Randomize

DBD = DbdApi()
STEAM = SteamApi()
UTILS = CommandUtils()

class DBDInfoClient(discord.Client):

    commands = {
        "-stats":Stats(STEAM, UTILS),
        "-screams":Screams(STEAM),
        "-escapes":Escapes(STEAM, UTILS),
        "-randomize":Randomize(DBD, UTILS)
    }

    async def on_ready(self):
        print(f'Logged on as {self.user}!') 
        # Not sure if this is the best way to handle the utils methods
        UTILS.set_pfp_url(self.user.display_avatar.url)

    async def on_message(self, message):

        if message.content.startswith("-"):
            args = message.content.split()
            arg_count = len(args)
            response = [None, None, None, None]

            # Help Command
            if args[0] == "-help":
                embed = UTILS.make_embed(UTILS.Color.NEUTRAL)
                embed.title = "DBD Info Bot Commands"
                embed.set_thumbnail(url=UTILS.pfp_url)

                for cmd in DBDInfoClient.commands.values():
                    embed.add_field(
                        name=cmd.name, 
                        value=cmd.description + "\nUsage: " + cmd.usage,
                        inline=False)
                
                response[1] = embed

            # Check if the command is valid
            elif args[0] not in DBDInfoClient.commands:
                response[0] = "Command " + args[0] + " not found!"

            else:
                command = DBDInfoClient.commands[args[0]]

                # Check if the proper number of arguments was given
                # Every command must have a field called num_args
                if arg_count < command.num_args:
                    response[0] = f"Missing arguments:\n\tUsage: " + command.usage

                else:
                    # Every command must have a run function that takes an array of arguments
                    # and returns a array that contains [message text, embed, embed_list, files_list], only one of which needs a value
                    response = command.run(args)
            
            await message.channel.send(content=response[0], embed=response[1], embeds=response[2], files=response[3])

intents = discord.Intents.default()
intents.message_content = True

client = DBDInfoClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))
