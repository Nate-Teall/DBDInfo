from discord import Embed
import re

# Returns a set of random perks for either killer or survivor
class Randomize:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "UTILS"]

    def __init__(self, DBD, UTILS):
        self.name = "randomize"
        self.description = "Gives a random perk set for survivor or killer, use -d to include descriptions"
        self.usage = "-randomize < killer | survivor > [-d]"
        self.num_args = 2

        self.DBD = DBD
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None]

        # Check if the user wants the perk descriptions included
        include_descriptions = len(args) > 2 and "d" in args[2]

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

            desc = self.cleanup_description(perk["description"], perk["tunables"]) if include_descriptions else ""

            # I would like to include images of perk icons, but mutliple images in a message/embed is not supported
            # Also, I'm not sure where to get a URL for the perk icons, I do not want to download all the images
            embed.add_field(name=perk_name, value=desc, inline=False)

        response[1] = embed
        return response
    
    def cleanup_description(self, desc, tunables):
        # Remove weird html tags
        desc = re.sub("<..?.?>", " ", desc)
        
        # Fill in tunables
        desc = desc.split()

        tunable = 0
        i = 0
        for word in desc:
            if word.startswith("{"):
                desc[i] = tunables[tunable].pop()
                tunable += 1
            i += 1

        desc = " ".join(desc)

        return desc 