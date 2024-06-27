from discord import Embed

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

        elif args[1].startswith("k"):
            perks = self.DBD.randomize("killer")

        else:
            response[0] = "Please specify 'survivor' or 'killer' \n\tUsage: " + self.usage
            return response
    
        #TODO: Finish this command. 
        #   I want to include perk images but have no idea how to include them without downloading all of them  

        embed1 = self.UTILS.make_embed()
        embed1.url = "https://google.com"
        embed1.set_image(url="https://dbd.tricky.lol/dbdassets/perks/2e1351c5165afbbec431b3f1a711546f92693a9e.png")

        embed2 = Embed()
        embed2.url = "https://google.com"
        embed2.set_image(url="https://dbd.tricky.lol/dbdassets/perks/2e1351c5165afbbec431b3f1a711546f92693a9e.png")

        embed3 = Embed()
        embed3.url = "https://google.com"
        embed3.set_image(url="https://dbd.tricky.lol/dbdassets/perks/2e1351c5165afbbec431b3f1a711546f92693a9e.png")

        embed4 = Embed()
        embed4.url = "https://google.com"
        embed4.set_image(url="https://dbd.tricky.lol/dbdassets/perks/2e1351c5165afbbec431b3f1a711546f92693a9e.png")

        response[1] = [embed1, embed2, embed3, embed4]

        return response