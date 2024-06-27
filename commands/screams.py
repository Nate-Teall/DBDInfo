# Scream command tells the user how many times the player has screamed as a Survivor
class Screams:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM"]

    def __init__(self, DBD, STEAM) -> None:
        self.name = "screams"
        self.description = "Provides the number of times a player has screamed as a survivor"
        self.usage = "-screams <steam-vanity-url>"
        self.num_args = 2

        self.DBD = DBD
        self.STEAM = STEAM

    def run(self, args):
        response = ["", None]
        try:
            vanity_url = args[1]
            player_id = self.STEAM.get_steam_id_64(vanity_url)
            scream_count = self.DBD.get_player_screams(player_id)

            response[0] = "Yikes! " + vanity_url + " has screamed " + str(scream_count) + " times! :scream:"

        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"
        
        return response