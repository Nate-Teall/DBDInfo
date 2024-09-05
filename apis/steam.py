import requests
import json
import os

# Handles requests to the steam API
class SteamApi:

    __slots__ = ["RESOLVE_VANITY_URL", "GET_PLAYER_SUMMARIES", "GET_STATS_FOR_GAME", "GET_OWNED_GAMES"]

    def __init__(self):
        api_key = os.getenv("STEAM_API_KEY")

        self.RESOLVE_VANITY_URL = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + api_key
        self.GET_PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + api_key
        self.GET_STATS_FOR_GAME = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=381210&key=" + api_key
        self.GET_OWNED_GAMES = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + api_key

    def get_steam_id_64(self, vanity_url_name):
        response = requests.get(self.RESOLVE_VANITY_URL + "&vanityurl=" + vanity_url_name)
        data = json.loads(response.text)["response"]

        if "steamid" not in data:
            print("Error: User with vanity url:", vanity_url_name, "not found.")
            raise ValueError

        return data["steamid"]
    
    def get_pfp_url(self, player_id):
        response = requests.get(self.GET_PLAYER_SUMMARIES + "&steamids=" + player_id)
        data = json.loads(response.text)["response"]["players"]

        # "data" is an array of all the players it found, if it is empty, none were found
        # realistically, this should never happen because the steamid64 provided here should
        #   be obtained from the "get_steam_id_64" method which will return a valid id if found
        if len(data) < 1:
            print("Error getting profile url for user:", player_id)
            raise ValueError
        
        return data[0]["avatarfull"]
    
    def get_dbd_data(self, player_id):
        response = requests.get(self.GET_STATS_FOR_GAME + "&steamid=" + player_id)

        if response.status_code >= 400:
            print("Error getting DBD stats from Steam for user:", player_id)
            raise ValueError
        
        data = json.loads(response.text)["playerstats"]

        # Steam gives the data as a list of key/value pairs, so it must be converted into a single dictionary
        data_dict = { stat["name"]:stat["value"] for stat in data["stats"] }
        # Add the number of the achievements the player has to this dictionary
        data_dict["achievements"] = len(data["achievements"])
        return data_dict
    
    def get_dbd_playtime(self, player_id):
        response = requests.get(self.GET_OWNED_GAMES + "&steamid=" + player_id)

        if response.status_code >= 400:
            print("Error getting Steam playtime for user:", player_id)
            raise ValueError
        
        #TODO: This line might be causing a key error with "games"
        games = json.loads(response.text)["response"]["games"]

        for game in games:
            if game["appid"] == 381210:
                return game["playtime_forever"]
        
        print("Could not find DBD in user's owned games")
        return 0

