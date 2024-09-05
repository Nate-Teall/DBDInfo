# Provides player statistics relating to a user's killer games
class Killer:
    __slots__ = ["name", "description", "usage", "num_args", "STEAM", "UTILS"]

    def __init__(self, STEAM, UTILS):
        self.name = "killer"
        self.description = "Gives more detailed stats about a player's killer games"
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
        
        # Killer overview includes: kills by hook, kills by mori or similar, matches won before the last gen repaired, survivors hooked in basement, survivors grabbed off gens, hatches closed
        kills_on_hook = player_stats["DBD_SacrificedCampers"] if "DBD_SacrificedCampers" in player_stats else 0
        kills_by_mori = player_stats["DBD_KilledCampers"] if "DBD_KilledCampers" in player_stats else 0
        games_won_quick = player_stats["DBD_Chapter11_Slasher_Stat1"] if "DBD_Chapter11_Slasher_Stat1" in player_stats else 0
        basement_hooks = player_stats["DBD_DLC6_Slasher_Stat2"] if "DBD_DLC6_Slasher_Stat2" in player_stats else 0
        hatches_closed = player_stats["DBD_Chapter13_Slasher_Stat1"] if "DBD_Chapter13_Slasher_Stat1" in player_stats else 0

        embed = self.UTILS.make_embed(self.UTILS.Color.KILLER)
        embed.title = "Killer stats for: " + display_name
        embed.set_thumbnail(url=player_pfp_url)

        embed.add_field(
            name="Kills on Hook:",
            value=kills_on_hook)
        
        embed.add_field(
            name="Kills not on Hook:",
            value=kills_by_mori)
        
        embed.add_field(
            name="Games Won Before Last Gen Completed:",
            value=games_won_quick)
        
        embed.add_field(
            name="Hatches Closed:",
            value=hatches_closed,
            inline=True)
        
        embed.add_field(
            name="Survivors Hooked in the Basement:",
            value=basement_hooks,
            inline=True)

        response[1] = embed
        return response
