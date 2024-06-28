from discord import Embed
import re

# Returns a set of random perks for either killer or survivor
class Randomize:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "UTILS"]

    def __init__(self, DBD, UTILS):
        self.name = "randomize"
        self.description = "Gives a random perk set for survivor or killer"
        self.usage = "-randomize < killer | survivor >"
        self.num_args = 2

        self.DBD = DBD
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None]

        if args[1].startswith("s"):
            perks = self.DBD.randomize("survivor")
            title = "Random Survivor Loadout:"

        elif args[1].startswith("k"):
            perks = self.DBD.randomize("killer")
            title = "Random Killer Loadout:"

        else:
            response[0] = "Please specify 'survivor' or 'killer' \n\tUsage: " + self.usage
            return response

        embed = self.UTILS.make_embed()
        embed.title = title

        for perk in perks.values():
            perk_name = perk["name"]
            
            # Descriptions are very long, I'll make it a separate option
            #desc = self.cleanup_description(perk["description"])
            desc = ""

            # I would like to include images of perk icons, but mutliple images in a message/embed is not supported
            # Also, I'm not sure where to get a URL for the perk icons, I do not want to download all the images
            embed.add_field(name=perk_name, value=desc, inline=False)

        response[1] = embed
        return response
    
    def cleanup_description(self, desc):
        # Remove weird html tags
        desc = re.sub("<..?.?>", " ", desc)

        return desc 