from discord import Embed, File
import re

# Returns a set of random perks for either killer or survivor
class Randomize:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "UTILS"]

    NIGHTLIGHT_URL = "https://cdn.nightlight.gg/img/perks/"

    def __init__(self, DBD, UTILS):
        self.name = "randomize"
        self.description = "Gives a random set of 1-4 perks for survivor or killer, use -d to include descriptions"
        self.usage = "-randomize < killer | survivor > [# of perks] [-d]"
        self.num_args = 2

        self.DBD = DBD
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None, None, None]

        # Check optional arguments 
        optional_args = args[2:]
        include_descriptions = "-d" in optional_args

        num_perks = int(optional_args[0]) if len(optional_args) > 0 and optional_args[0].isnumeric() else 4
        if num_perks < 1 or num_perks > 4:
            num_perks = 4

        if args[1].startswith("s"):
            perks = self.DBD.randomize("survivor")
            title = "Random Survivor Perk:"
            embed_color = self.UTILS.Color.SURVIVOR.value

        elif args[1].startswith("k"):
            perks = self.DBD.randomize("killer")
            title = "Random Killer Perk:"
            embed_color = self.UTILS.Color.KILLER.value

        else:
            response[0] = "Please specify 'survivor' or 'killer' \n\tUsage: " + self.usage
            return response

        # perks.values() gives a view, we must cast it to a list
        perks = list(perks.values())
        
        embed_list = []

        for i in range(num_perks):
            perk = perks[i]

            embed = Embed(title=perk["name"], color=embed_color)
            embed.set_author(name=title, icon_url=self.UTILS.pfp_url)

            desc = self.cleanup_description(perk["description"], perk["tunables"]) if include_descriptions else ""
            embed.description = desc

            icon_path = perk["image"]
            icon_url = get_url(icon_path)

            #print("Using url:", icon_url)
            embed.set_thumbnail(url=icon_url)

            embed_list.append(embed)

        response[2] = embed_list
        return response
    
    def cleanup_description(self, desc, tunables):
        # Remove weird html tags
        # Possibly, replace the bold/italicize/newline tags with their markdown counterpart
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

def get_url(path):
    split_path = path.split("/")

    # tricky.lol gives the filepath of the perk, and the name is "iconPerks_<name>"
    # nightlight.gg urls do not include the "iconPerks_" part
    icon_name = split_path.pop().split("_").pop()
    # nightlight perks are in camelcase
    # BUT sometimes they arent... NIGHTLIGHT IS NOT RELIABLE RAHHHHH
    icon_name = icon_name[:1].lower() + icon_name[1:]

    # nightlight urls also do not include the "UI/icons" at the beginning of the filepath
    return Randomize.NIGHTLIGHT_URL + "/".join(split_path[3:]) + "/" + icon_name