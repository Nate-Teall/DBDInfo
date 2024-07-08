# Scream command tells the user how many times the player has screamed as a Survivor
class Screams:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM"]

    def __init__(self, STEAM):
        self.name = "screams"
        self.description = "Provides the number of times a player has screamed as a survivor"
        self.usage = "-screams <steam-vanity-url>"
        self.num_args = 2

        self.STEAM = STEAM

    def run(self, args):
        response = [None, None, None, None]

        try:
            vanity_url = args[1]
            player_id = self.STEAM.get_steam_id_64(vanity_url)

            steam_data = self.STEAM.get_dbd_data(player_id)
            player_stats = { stat["name"]:stat["value"] for stat in steam_data["stats"] }
            scream_count = player_stats["DBD_Camper38_Stat2"] if "DBD_Camper38_Stat2" in player_stats else 0

            response[0] = "Yikes! " + vanity_url + " has screamed " + str(scream_count) + " times! :scream:"

        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"
        
        return response