from discord import Embed

# Extra file for any functions that multiple commands may need
class CommandUtils:
    __slots__ = ["pfp_url"]

    def set_pfp_url(self, pfp_url):
        self.pfp_url = pfp_url

    def make_embed(self) -> Embed:
        embed = Embed(type="rich", color=0x60008a)
        embed.set_author(name="DBD Info Bot", url="https://github.com/Nate-Teall/DBDInfo", icon_url=self.pfp_url)
        embed.set_footer(text="See you in the fog...")

        return embed