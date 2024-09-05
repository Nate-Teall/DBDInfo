# Scream command tells the user how many times the player has screamed as a Survivor
class Screams:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM"]

    def __init__(self, STEAM):
        self.name = "screams"
        self.description = "Provides the number of times a player has screamed as a survivor"
        self.usage = "-screams <steamID | steam-vanity-url>"
        self.num_args = 2

        self.STEAM = STEAM

    def run(self, args):
        response = [None, None, None, None]

        try:
            player_id = self.STEAM.get_steam_id_64(args[1])
        except ValueError:
            player_id = args[1]

        try:
            player_summary = self.STEAM.get_player_summary(player_id)
            display_name = player_summary["personaname"]

            player_stats = self.STEAM.get_dbd_data(player_id)
            scream_count = player_stats["DBD_Camper38_Stat2"] if "DBD_Camper38_Stat2" in player_stats else 0

            response[0] = "Yikes! " + display_name + " has screamed " + str(scream_count) + " times! :scream:"

        except ValueError:
            response[0] = "Player with ID or vanity URL: " + args[1] + " not found! User may not have played DBD previously."
        
        return response