# Provides player statistics relating to a user's survivor games
class Survivor:
    __slots__ = ["name", "description", "usage", "num_args", "STEAM", "UTILS"]

    def __init__(self, STEAM, UTILS):
        self.name = "survivor"
        self.description = "Gives more detailed stats about a player's survivor games"
        self.usage = "-survivor <steamID | steam-vanity-url>"
        self.num_args = 2

        self.STEAM = STEAM
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None, None, None]

        try:
            player_id = self.STEAM.get_steam_id_64(args[1])
        except ValueError:
            player_id = args[1]

        try:
            player_summary = self.STEAM.get_player_summary(player_id)
            display_name = player_summary["personaname"]
            player_pfp_url = player_summary["avatarfull"]

            player_stats = self.STEAM.get_dbd_data(player_id)
        
        except ValueError:
            response[0] = "Player with ID or vanity URL: " + args[1] + " not found!"
            return response
        
        # Survivor overview includes: Gens completed, survivors healed, exit gates opened, totems cleansed, self unhooks, survivors unhooked, successful skillchecks
        gens = player_stats["DBD_GeneratorPct_float"] if "DBD_GeneratorPct_float" in player_stats else 0
        heals = player_stats["DBD_HealPct_float"] if "DBD_HealPct_float" in player_stats else 0
        gates = player_stats["DBD_DLC7_Camper_Stat2"] if "DBD_DLC7_Camper_Stat2" in player_stats else 0
        unhook_or_heal_from_dying = player_stats["DBD_UnhookOrHeal"] if "DBD_UnhookOrHeal" in player_stats else 0
        heal_from_dying = player_stats["DBD_Chapter15_Camper_Stat1"] if "DBD_Chapter15_Camper_Stat1" in player_stats else 0
        totems = player_stats["DBD_DLC3_Camper_Stat1"] if "DBD_DLC3_Camper_Stat1" in player_stats else 0
        skill_checks = player_stats["DBD_SkillCheckSuccess"] if "DBD_SkillCheckSuccess" in player_stats else 0
        self_unhooks = player_stats["DBD_Chapter9_Camper_Stat1"] if "DBD_Chapter9_Camper_Stat1" in player_stats else 0

        embed = self.UTILS.make_embed(self.UTILS.Color.SURVIVOR)
        embed.title = "Survivor stats for: " + display_name
        embed.set_thumbnail(url=player_pfp_url)

        embed.add_field(
            name="Generators Completed:", 
            value=str(round(gens, 1)))

        embed.add_field(
            name="Survivors Healed:", 
            value=str(round(heals, 1)))

        embed.add_field(
            name="Exit Gates Opened:", 
            value=gates)
        
        # For some reason steam stores two stats, one being survivors unhooked OR healed from dying state,
        # the other being survivors healed from dying state 
        # So, I have to use both of these to get the total number of survivors unhooked
        embed.add_field(
            name="Survivors Unhooked:",
            value=unhook_or_heal_from_dying - heal_from_dying,
            inline=True)
        
        embed.add_field(
            name="Totems Cleansed:",
            value=totems,
            inline=True)
        
        embed.add_field(
            name="Successful Skill Checks:",
            value=skill_checks,
            inline=True)
        
        embed.add_field(
            name="Self Unhooks:",
            value=self_unhooks,
            inline=True)
        
        response[1] = embed
        return response