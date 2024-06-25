import discord
import os

from dbd import DbdApi
from steam import SteamApi

DBD = DbdApi()
STEAM = SteamApi()

class MyClient(discord.Client):

    __slots__ = ["pfp_url"]

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

    async def on_ready(self):
        print(f'Logged on as {self.user}!') 
        self.pfp_url = self.user.display_avatar.url

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

                        await message.channel.send("Yikes! " + vanity_url + " has screamed " + str(scream_count) + " times! :scream:")

                    except ValueError:
                        await message.channel.send("Player: " + vanity_url + " not found!")
                    
                case "-escapes":
                    try:
                        vanity_url = params[1]
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
                        vanity_url = params[1]
                        player_id = STEAM.get_steam_id_64(vanity_url)
                        bloodpoints, playtime = DBD.player_overview(player_id)
                        steam_data = STEAM.get_dbd_data(player_id)
                        player_pfp_url = STEAM.get_pfp_url(player_id)

                        # Steam gives the data as a list of json objects, the 28th of which gives the stat we're looking for
                        # Because they are all separate json objects in a list, I cannot simply use the dictionary key to find it
                        most_bp = steam_data["stats"][27]["value"]
                        ach = len(steam_data["achievements"])
                        killer_pip = steam_data["stats"][0]["value"]
                        surv_pip = steam_data["stats"][1]["value"]

                        embed = self.make_embed()
                        embed.title = "Overview for: " + vanity_url
                        embed.set_thumbnail(url=player_pfp_url)
                        embed.add_field(name="Playtime:", value=str(playtime/60) + " hours")
                        embed.add_field(name="Total Bloodpoints:", value=bloodpoints)
                        embed.add_field(name="Most BP Spent on one character:", value=most_bp)
                        embed.add_field(
                            name="Achievements:", 
                            value=str(ach) + " / " + str(self.total_achievements) + " (" + str(ach/self.total_achievements) + "%)",
                            inline=True)
                        embed.add_field(
                            name="Survivor Grade:",
                            value=self.calculate_rank(surv_pip) + " (" + str(surv_pip) + " pips)",
                            inline=True)
                        embed.add_field(
                            name="Killer Grade:",
                            value=self.calculate_rank(killer_pip) + " (" +str(killer_pip) + " pips)",
                            inline=True)
                        
                        await message.channel.send(embed=embed)

                    except ValueError:
                        await message.channel.send("Player: " + vanity_url + " not found!")
                case _: 
                    return

    def make_embed(self):
        embed = discord.Embed(type="rich", color=0x60008a)
        embed.set_author(name="DBD Info Bot", url="https://github.com/Nate-Teall/DBDInfo", icon_url=self.pfp_url)
        embed.set_footer(text="See you in the fog...")

        return embed
    
    # Helper function to calculate the survivor/killer grade from the number of pips (gold I, iri III, ash IV, etc...)
    def calculate_rank(self, pips):
        grade = ""

        # Ash IV - III
        if pips < 6:
            grade = self.grade_strings[ pips // 3 ]
        # Ash II - Bronze I
        elif pips < 30:
            grade = self.grade_strings[ 2 + (pips-6) // 4 ]
        # Silver IV - Iri I
        else:
            grade = self.grade_strings[ 8 + (pips-22) // 5 ]

        return grade


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))

#if __name__ == "__main__":
#    main()