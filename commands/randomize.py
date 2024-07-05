from discord import Embed, File
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
        response = [None, None, None, 1]

        # Check if the user wants the perk descriptions included
        include_descriptions = len(args) > 2 and "d" in args[2]

        if args[1].startswith("s"):
            perks = self.DBD.randomize("survivor")
            title = "Random Survivor Perk:"
            embed_color = 0x52a5ff

        elif args[1].startswith("k"):
            perks = self.DBD.randomize("killer")
            title = "Random Killer Perk:"
            embed_color = 0xff4040

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
            icon_name = icon_path.split("/").pop()
            try:
                file = File(icon_path, filename=icon_name)   
                embed.set_thumbnail(url="attachment://" + icon_name)
                file_list.append(file)
            except FileNotFoundError:
                print("Missing perk icon for:", perk["name"], " . Might need to download new icons")

            embed_list.append(embed)

        response[2] = embed_list
        response[3] = file_list
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