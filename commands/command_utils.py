from discord import Embed
from enum import Enum

# Extra file for any functions that multiple commands may need
class CommandUtils:
    __slots__ = ["pfp_url"]

    # This color enum is probably unecessary, but I think it makes it cleaner to define which colors are used in a single place
    class Color(Enum):
        SURVIVOR = 0x52a5ff
        KILLER = 0xff4040
        NEUTRAL = 0xe252ff


    def set_pfp_url(self, pfp_url):
        self.pfp_url = pfp_url

    def make_embed(self, embed_color) -> Embed:
        embed = Embed(type="rich", color=embed_color.value)
        embed.set_author(name="DBD Info Bot", url="https://github.com/Nate-Teall/DBDInfo", icon_url=self.pfp_url)
        embed.set_footer(text="See you in the fog...")

        return embed