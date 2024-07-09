from discord import Embed, File
import re

# Returns a set of random perks for either killer or survivor
class Randomize:
    __slots__ = ["name", "description", "usage", "num_args", "DBD", "UTILS"]

    NIGHTLIGHT_URL = "https://cdn.nightlight.gg/img/"

    def __init__(self, DBD, UTILS):
        self.name = "randomize"
        self.description = "Gives a random perk set for survivor or killer, use -d to include descriptions"
        self.usage = "-randomize < killer | survivor > [-d]"
        self.num_args = 2

        self.DBD = DBD
        self.UTILS = UTILS

    def run(self, args):
        response = [None, None, None, None]

        # Check if the user wants the perk descriptions included
        include_descriptions = len(args) > 2 and "d" in args[2]

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

        
        embed_list = []
        file_list = []

        for perk in perks.values():
            embed = Embed(title=perk["name"], color=embed_color)
            embed.set_author(name=title, icon_url=self.UTILS.pfp_url)

            desc = self.cleanup_description(perk["description"], perk["tunables"]) if include_descriptions else ""
            embed.description = desc

            icon_path = perk["image"]
            icon_url = get_url(icon_path)

            """ icon_name = icon_path.split("/").pop()
            try:
                file = File(icon_path, filename=icon_name)
                embed.set_thumbnail(url="attachment://" + icon_name)
                file_list.append(file)
            except FileNotFoundError:
                print("Missing perk icon for:", perk["name"], " . Might need to download new icons") """

            embed.set_thumbnail(url="icon_url")

            embed_list.append(embed)

        response[2] = embed_list
        #response[3] = file_list
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
    icon_name = split_path.pop().split("_")[1]

    # nightlight urls also do not include the "UI/icons" at the beginning of the filepath
    return randomize.NIGHTLIGHT_URL + "/".join(split_path[2:]) + "/" + icon_name