# Provides player statistics relating to a user's survivor games
class Survivor:
    __slots__ = ["name", "description", "usage", "num_args", "STEAM", "UTILS"]

    def __init__(self, STEAM, UTILS):
        self.name = "survivor"
        self.description = "Gives more detailed stats about a player's survivor games"
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

            steam_data = self.STEAM.get_dbd_data(player_id)
        
        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"
            return response