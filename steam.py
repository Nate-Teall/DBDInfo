import requests
import json
import os

# Handles requests to the steam API
class SteamApi:

    __slots__ = ["STEAM_RESOLVE_VANITY_URL"]

    def __init__(self):
        self.STEAM_RESOLVE_VANITY_URL = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + os.getenv("STEAM_API_KEY")

    def get_steam_id_64(self, vanity_url_name):
        response = requests.get(self.STEAM_RESOLVE_VANITY_URL + "&vanityurl=" + vanity_url_name)
        data = json.loads(response.text)["response"]

        if "steamid" not in data:
            print("Error: User with vanity url:", vanity_url_name, "not found.")
            raise ValueError

        return data["steamid"]