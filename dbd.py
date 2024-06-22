import requests
import json

# Handles requests to the dbd.tricky.lol API
class DbdApi:

    __slots__ = ["DBD_URL"]

    def __init__(self):
        self.DBD_URL = "https://dbd.tricky.lol/api/"

    # makes the request for player data, given the user's SteamID64 as a string
    # should be by player's steam name (soon)
    def get_player_screams(self, player_id):
        response = requests.get(self.DBD_URL + "playerstats?steamid=" + player_id)

        # Keeping this try response in case a player exists, but has not played DBD
        if response.status_code == 404:
            print("Error: User", player_id, "not found. They likely have not played DBD!")
            raise ValueError

        data = json.loads(response.text)
        
        return data["screams"]
