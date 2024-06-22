import requests
import json

DBD_URL = "https://dbd.tricky.lol/api/"

# Handles requests to the dbd.tricky.lol API
class DbdApi:

    __slots__ = ["player_data", "player_name"]

    def __init__(self):
        self.player_data = None
        self.player_name = None

    # makes the request for player data, given the user's SteamID64 as a string
    # should be by player's steam name (soon)
    def get_player_stats(self, player_id):
        data = requests.get(DBD_URL + "playerstats?steamid=" + player_id)

        if data.status_code == 404:
            raise ValueError("Error: User", player_id, "not found.") 

        self.player_data = json.loads(data.text)
        self.player_name = player_id
