# Provides a user's information about the number of escapes they have completed as a survivor
class Escapes:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM", "UTILS"]

    def __init__(self, STEAM, UTILS):
        self.name = "escapes"
        self.description = "Gives information about the number of times a player has escaped the trial"
        self.usage = "-escapes <steam-vanity-url>"
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
            player_stats = { stat["name"]:stat["value"] for stat in steam_data["stats"] }

            # Unsure if this first stat is TOTAL escapes for escapes while healthy/injured
            escapes = player_stats["DBD_Escape"] if "DBD_Escape" in player_stats else 0
            escapes_ko = player_stats["DBD_EscapeKO"] if "DBD_EscapeKO" in player_stats else 0
            escapes_hatch = player_stats["DBD_EscapeThroughHatch"] if "DBD_EscapeThroughHatch" in player_stats else 0

            embed_desc = "Escapes while healthy/injured: " + str(escapes) + "\n"\
                         "Escapes through hatch: " + str(escapes_hatch) + "\n"\
                         "Escapes while downed: " + str(escapes_ko) + "\n"\
                                     
            embed = self.UTILS.make_embed(self.UTILS.Color.SURVIVOR)
            embed.title = "Survivor escapes for " + vanity_url
            embed.description = embed_desc
            embed.set_thumbnail(url=player_pfp_url)
                    
            response[1] = embed

        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"

        return response