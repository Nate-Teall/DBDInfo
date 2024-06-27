# Provides a general overview of a user, including playtime, player level, bloodpoints, grades, and more
class Stats:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM", "UTILS"]
    
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

    def __init__(self, DBD, STEAM, UTILS):
        self.name = "stats"
        self.description = "Gives general information about a player, including playtime, level, grades, and more"
        self.usage = "-stats <steam-vanity-url>"
        self.num_args = 2

        self.DBD = DBD
        self.STEAM = STEAM
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None]

        # Overview includes: total BP, playtime, Most BP on a single char, grades, ach. progress
        try:
            vanity_url = args[1]
            player_id = self.STEAM.get_steam_id_64(vanity_url)
            bloodpoints, playtime = self.DBD.player_overview(player_id)
            steam_data = self.STEAM.get_dbd_data(player_id)
            player_pfp_url = self.STEAM.get_pfp_url(player_id)

            # Steam gives the data as a list of json objects, the 28th of which gives the stat we're looking for
            # Because they are all separate json objects in a list, I cannot simply use the dictionary key to find it
            # NOTE: THIS DOES NOT WORK FOR ALL USERS. MOST_BP SEEMS TO BREAK
            most_bp = steam_data["stats"][27]["value"]
            ach = len(steam_data["achievements"])
            killer_pip = steam_data["stats"][0]["value"]
            surv_pip = steam_data["stats"][1]["value"]

            embed = self.UTILS.make_embed()
            embed.title = "Overview for: " + vanity_url
            embed.set_thumbnail(url=player_pfp_url)
            embed.add_field(name="Playtime:", value=str(round(playtime/60, 1)) + " hours")

            bp_str = f'{bloodpoints:,}' 
            embed.add_field(name="Total Bloodpoints:", value=bp_str)

            most_bp_str = f'{most_bp:,}'
            embed.add_field(name="Most BP Spent on one character:", value=most_bp_str)

            ach_pct = str( round((ach / Stats.total_achievements) * 100, 2) )
            embed.add_field(
                name="Achievements:", 
                value=str(ach) + " / " + str(Stats.total_achievements) + " (" + ach_pct + "%)",
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
                        
            response[1] = embed

        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"

        return response
    
    # Helper function to calculate the survivor/killer grade from the number of pips (gold I, iri III, ash IV, etc...)
    def calculate_rank(self, pips):
        grade = ""
        remainder = 0

        # Ash IV - III
        if pips < 6:
            grade = Stats.grade_strings[ pips // 3 ]
            remainder = pips % 3

        # Ash II - Bronze I
        elif pips < 30:
            grade = Stats.grade_strings[ 2 + (pips-6) // 4 ]
            remainder = (pips-6) % 4

        # Silver IV - Iri I
        else:
            grade = Stats.grade_strings[ 8 + (pips-30) // 5 ]
            remainder = (pips-30) % 5

        return grade, str(remainder)
