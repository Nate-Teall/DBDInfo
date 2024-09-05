# Provides a user's information about the number of escapes they have completed as a survivor
class Escapes:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM", "UTILS"]

    def __init__(self, STEAM, DBD, UTILS):
        self.name = "escapes"
        self.description = "Gives information about the number of times a player has escaped the trial"
        self.usage = "-escapes <steamID | steam-vanity-url>"
        self.num_args = 2

        self.STEAM = STEAM
        self.UTILS = UTILS
        self.DBD = DBD

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
            tricky_data = self.DBD.get_player_data(player_id)

        except ValueError:
            response[0] = "Player with ID or vanity URL: " + args[1] + " not found!"
            return response

        # Unsure if this first stat is TOTAL escapes for escapes while healthy/injured
        escapes = player_stats["DBD_Escape"] if "DBD_Escape" in player_stats else 0
        escapes_ko = player_stats["DBD_EscapeKO"] if "DBD_EscapeKO" in player_stats else 0
        escapes_hatch = player_stats["DBD_EscapeThroughHatch"] if "DBD_EscapeThroughHatch" in player_stats else 0
        escaped_newitem = tricky_data["escaped_newitem"]

        embed_desc = "Escapes while healthy/injured: " + str(escapes) + "\n"\
                        "Escapes through hatch: " + str(escapes_hatch) + "\n"\
                        "Escapes while downed: " + str(escapes_ko) + "\n"\
                        "Escapes with another player's item: " + str(escaped_newitem) + "\n"
                                    
        embed = self.UTILS.make_embed(self.UTILS.Color.SURVIVOR)
        embed.title = "Survivor escapes for " + display_name
        embed.description = embed_desc
        embed.set_thumbnail(url=player_pfp_url)
                
        response[1] = embed

        return response