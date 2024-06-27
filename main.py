import discord
import os

from apis.dbd import DbdApi
from apis.steam import SteamApi

from commands.command_utils import CommandUtils
from commands.screams import Screams
from commands.escapes import Escapes

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
            return

            match args[0]:
                # Get a player's total times screamed from their vanity url name. 
                # Not yet sure how to get steam id by username 
                case "-screams": 
                    try:
                        vanity_url = args[1]
                        player_id = STEAM.get_steam_id_64(vanity_url)
                        scream_count = DBD.get_player_screams(player_id)

                        await message.channel.send("Yikes! " + vanity_url + " has screamed " + str(scream_count) + " times! :scream:")

                    except ValueError:
                        await message.channel.send("Player: " + vanity_url + " not found!")
                    
                case "-escapes":
                    try:
                        vanity_url = args[1]
                        player_id = STEAM.get_steam_id_64(vanity_url)
                        escaped, escaped_ko, escaped_hatch = DBD.get_escape_data(player_id)
                        player_pfp_url = STEAM.get_pfp_url(player_id)

                        embed_desc = "Total Escapes: " + str(escaped) + "\n"\
                                     "Escapes through hatch: " + str(escaped_hatch) + "\n"\
                                     "Escapes while downed: " + str(escaped_ko) + "\n"\
                                     
                        embed = self.make_embed()
                        embed.title = "Survivor escapes for " + vanity_url
                        embed.description = embed_desc
                        embed.set_thumbnail(url=player_pfp_url)
                    
                        await message.channel.send(embed=embed)

                    except ValueError:
                        await message.channel.send("Player: " + vanity_url + " not found!")
                
                case "-stats":
                    # Overview includes: total BP, playtime, Most BP on a single char, grades, ach. progress
                    try:
                        vanity_url = args[1]
                        player_id = STEAM.get_steam_id_64(vanity_url)
                        bloodpoints, playtime = DBD.player_overview(player_id)
                        steam_data = STEAM.get_dbd_data(player_id)
                        player_pfp_url = STEAM.get_pfp_url(player_id)

                        # Steam gives the data as a list of json objects, the 28th of which gives the stat we're looking for
                        # Because they are all separate json objects in a list, I cannot simply use the dictionary key to find it
                        # NOTE: THIS DOES NOT WORK FOR ALL USERS. MOST_BP SEEMS TO BREAK
                        most_bp = steam_data["stats"][27]["value"]
                        ach = len(steam_data["achievements"])
                        killer_pip = steam_data["stats"][0]["value"]
                        surv_pip = steam_data["stats"][1]["value"]

                        embed = self.make_embed()
                        embed.title = "Overview for: " + vanity_url
                        embed.set_thumbnail(url=player_pfp_url)
                        embed.add_field(name="Playtime:", value=str(round(playtime/60, 1)) + " hours")

                        bp_str = f'{bloodpoints:,}' 
                        embed.add_field(name="Total Bloodpoints:", value=bp_str)

                        most_bp_str = f'{most_bp:,}'
                        embed.add_field(name="Most BP Spent on one character:", value=most_bp_str)

                        ach_pct = str( round((ach / self.total_achievements) * 100, 2) )
                        embed.add_field(
                            name="Achievements:", 
                            value=str(ach) + " / " + str(self.total_achievements) + " (" + ach_pct + "%)",
                            inline=True)
                        
                        surv_grade, surv_remainder = self.calculate_rank(surv_pip)
                        embed.add_field(
                            name="Survivor Grade:",
                            value=surv_grade + ", " + surv_remainder + " pips",
                            inline=True)
                        
                        killer_grade, killer_remainer = self.calculate_rank(killer_pip)
                        embed.add_field(
                            name="Killer Grade:",
                            value=killer_grade + ", " + killer_remainer + " pips",
                            inline=True)
                        
                        await message.channel.send(embed=embed)

                    except ValueError:
                        await message.channel.send("Player: " + vanity_url + " not found!")
                case _: 
                    return
    
    # Helper function to calculate the survivor/killer grade from the number of pips (gold I, iri III, ash IV, etc...)
    def calculate_rank(self, pips):
        grade = ""
        remainder = 0

        # Ash IV - III
        if pips < 6:
            grade = self.grade_strings[ pips // 3 ]
            remainder = pips % 3

        # Ash II - Bronze I
        elif pips < 30:
            grade = self.grade_strings[ 2 + (pips-6) // 4 ]
            remainder = (pips-6) % 4

        # Silver IV - Iri I
        else:
            grade = self.grade_strings[ 8 + (pips-30) // 5 ]
            remainder = (pips-30) % 5

        return grade, str(remainder)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))