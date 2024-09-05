# Provides player statistics relating to a user's killer games
class Killer:
    __slots__ = ["name", "description", "usage", "num_args", "STEAM", "UTILS"]

    def __init__(self, STEAM, UTILS):
        self.name = "killer"
        self.description = "Gives more detailed stats about a player's killer games"
        self.usage = "-survivor <steam-vanity-url>"
        self.num_args = 2

        self.STEAM = STEAM
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None, None, None]

        try:
            vanity_url = args[1]
            player_id = self.STEAM.get_steam_id_64(vanity_url)

            player_pfp_url = self.STEAM.get_pfp_url(player_id)

            player_stats = self.STEAM.get_dbd_data(player_id)

        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"
            return response
        
        # Killer overview includes: kills by hook, kills by mori or similar, matches won before the last gen repaired, survivors hooked in basement, survivors grabbed off gens, hatches closed
        kills_on_hook = player_stats["DBD_SacrificedCampers"] if "DBD_SacrificedCampers" in player_stats else 0
        kills_by_mori = player_stats["DBD_KilledCampers"] if "DBD_KilledCampers" in player_stats else 0
        games_won_quick = player_stats["DBD_Chapter11_Slasher_Stat1"] if "DBD_Chapter11_Slasher_Stat1" in player_stats else 0
        basement_hooks = player_stats["DBD_DLC6_Slasher_Stat2"] if "DBD_DLC6_Slasher_Stat1" in player_stats else 0
        hatches_closed = player_stats["DBD_Chapter13_Slasher_Stat1"] if "DBD_Chapter13_Slasher_Stat1" in player_stats else 0

        embed = self.UTILS.make_embed(self.UTILS.Color.KILLER)
        embed.title = "Killer stats for: " + vanity_url
        embed.set_thumbnail(url=player_pfp_url)

        response[1] = embed
        return response
