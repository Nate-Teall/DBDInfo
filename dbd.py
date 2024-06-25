import requests
import json

# Handles requests to the dbd.tricky.lol API
class DbdApi:

    __slots__ = ["DBD_URL"]

    def __init__(self):
        self.DBD_URL = "https://dbd.tricky.lol/api/"

    def get_player_data(self, player_id):
        response = requests.get(self.DBD_URL + "playerstats?steamid=" + player_id)

        # If no data was found, the user either has not played DBD, or their profile is set to private
        if response.status_code == 404:
            print("Error: User", player_id, "not found. They likely have not played DBD, or their steam profile is private.")
            raise ValueError
        
        return json.loads(response.text)

    # makes the request for player data, given the user's SteamID64 as a string
    # should be by player's steam name (soon)
    def get_player_screams(self, player_id):
        data = self.get_player_data(player_id)
        
        return data["screams"]

    def get_escape_data(self, player_id):
        data = self.get_player_data(player_id)

        return data["escaped"], data["escaped_ko"], data["escaped_hatch"]
    
    def player_overview(self, player_id):
        data = self.get_player_data(player_id)

        return data["bloodpoints"], data["playtime"], data["survivor_rank"], data["killer_rank"]