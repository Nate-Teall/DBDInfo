# Provides a user's information about the number of escapes they have completed as a survivor
class Escapes:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "STEAM", "UTILS"]

    def __init__(self, DBD, STEAM, UTILS):
        self.name = "escapes"
        self.description = "Gives information about the number of times a player has escaped the trial"
        self.usage = "-escapes <steam-vanity-url>"
        self.num_args = 2

        self.DBD = DBD
        self.STEAM = STEAM
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None, None, None]

        try:
            vanity_url = args[1]
            player_id = self.STEAM.get_steam_id_64(vanity_url)
            escaped, escaped_ko, escaped_hatch = self.DBD.get_escape_data(player_id)
            player_pfp_url = self.STEAM.get_pfp_url(player_id)

            embed_desc = "Total Escapes: " + str(escaped) + "\n"\
                         "Escapes through hatch: " + str(escaped_hatch) + "\n"\
                         "Escapes while downed: " + str(escaped_ko) + "\n"\
                                     
            embed = self.UTILS.make_embed()
            embed.title = "Survivor escapes for " + vanity_url
            embed.description = embed_desc
            embed.set_thumbnail(url=player_pfp_url)
                    
            response[1] = embed

        except ValueError:
            response[0] = "Player: " + vanity_url + " not found!"

        return response