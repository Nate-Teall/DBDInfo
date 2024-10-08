# Provides a general overview of a user, including playtime, player level, bloodpoints, grades, and more
class Stats:
    __slots__ = ["name", "description", "usage", "num_args", "STEAM", "UTILS"]
    
    # This shouldn't be hard coded, I will find a way to get the total number of achievements from steam.
    total_achievements = 264
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

    def __init__(self, STEAM, UTILS):
        self.name = "stats"
        self.description = "Gives general information about a player, including playtime, level, grades, and more"
        self.usage = "-stats <steamID | steam-vanity-url>"
        self.num_args = 2

        self.STEAM = STEAM
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None, None, None]

        # First, try turning the given argument into an ID, assuming it is a vanity url
        try:
            player_id = self.STEAM.get_steam_id_64(args[1])
        except ValueError:
            # If that doesn't work, we will assume the user gave a valid steam ID
            player_id = args[1]

        try:
            player_summary = self.STEAM.get_player_summary(player_id)
            display_name = player_summary["personaname"]
            player_pfp_url = player_summary["avatarfull"]

            playtime = self.STEAM.get_dbd_playtime(player_id)

            player_stats = self.STEAM.get_dbd_data(player_id)
        
        except ValueError:
            # If the given argument still doesn't work, abort
            response[0] = "Player with ID or vanity URL: " + args[1] + " not found! User may not have played DBD previously."
            return response

        # Overview includes: total BP, playtime, Most BP on a single char, grades, ach. progress
        # I have to add this extra "if" because if a stat is 0, then it simply doesn't appear in the response
        total_bp = player_stats["DBD_BloodwebPoints"] if "DBD_BloodwebPoints" in player_stats else 0
        most_bp = player_stats["DBD_MaxBloodwebPointsOneCategory"] if "DBD_MaxBloodwebPointsOneCategory" in player_stats else 0
        ach = player_stats["achievements"]
        killer_pip = player_stats["DBD_KillerSkulls"] if "DBD_KillerSkulls" in player_stats else 0
        surv_pip = player_stats["DBD_CamperSkulls"] if "DBD_CamperSkulls" in player_stats else 0

        embed = self.UTILS.make_embed(self.UTILS.Color.NEUTRAL)
        embed.title = "Overview for: " + display_name
        embed.set_thumbnail(url=player_pfp_url)
        embed.add_field(name="Playtime:", value=str(round(playtime/60, 1)) + " hours")

        bp_str = f'{total_bp:,}' 
        embed.add_field(name="Total Bloodpoints:", value=bp_str)

        most_bp_str = f'{most_bp:,}'
        embed.add_field(name="Most BP Spent on One Character:", value=most_bp_str)

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
                    
        killer_grade, killer_remainder = self.calculate_rank(killer_pip)
        embed.add_field(
            name="Killer Grade:",
            value=killer_grade + ", " + killer_remainder + " pips",
            inline=True)
                    
        response[1] = embed

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
