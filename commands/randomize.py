# Returns a set of random perks for either killer or survivor
class Randomize:
    __slots__ = ["name", "description", "usage", "num_args", "DBD"]

    def __init__(self, DBD):
        self.name = "randomize"
        self.description = "Gives a random perk set for survivor or killer"
        self.usage = "-randomize < killer | survivor >"
        self.num_args = 2

        self.DBD = DBD

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

        return response