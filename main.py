import discord
import os

from dbd import DbdApi
from steam import SteamApi

DBD = DbdApi()
STEAM = SteamApi()

class MyClient(discord.Client):

    __slots__ = ["pfp_url"]

    # This shouldn't be hard coded, I will find a way to get the total number of achievements from steam.
    total_achievements = "255"

    async def on_ready(self):
        print(f'Logged on as {self.user}!') 
        self.pfp_url = self.user.display_avatar.url

    def make_embed(self):
        embed = discord.Embed(type="rich", color=0x60008a)
        embed.set_author(name="DBD Info Bot", url="https://github.com/Nate-Teall/DBDInfo", icon_url=self.pfp_url)
        embed.set_footer(text="See you in the fog...")

        return embed

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
                        bloodpoints, playtime, survivor_rank, killer_rank = DBD.player_overview(player_id)
                        steam_data = STEAM.get_dbd_data(player_id)
                        player_pfp_url = STEAM.get_pfp_url(player_id)

                        # Steam gives the data as a list of json objects, the 28th of which gives the stat we're looking for
                        # Because they are all separate json objects in a list, I cannot simply use the dictionary key to find it
                        most_bp = steam_data["stats"][27]["value"]
                        ach = len(steam_data["achievements"])

                        embed = self.make_embed()
                        embed.title = "Overview for: " + vanity_url
                        embed.set_thumbnail(url=player_pfp_url)
                        embed.add_field(name="Playtime:", value=str(playtime/60) + " hours")
                        embed.add_field(name="Total Bloodpoints:", value=bloodpoints)
                        embed.add_field(name="Most BP Spent on one character:", value=most_bp)
                        embed.add_field(
                            name="Achievements:", 
                            value=str(ach) + " / " + self.total_achievements + " achievements",
                            inline=True)
                        embed.add_field(
                            name="Survivor Grade:",
                            value=str(survivor_rank) + " pips",
                            inline=True)
                        embed.add_field(
                            name="Killer Grade:",
                            value=str(killer_rank) + " pips",
                            inline=True)
                        
                        await message.channel.send(embed=embed)

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