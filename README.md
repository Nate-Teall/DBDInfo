# DBD Info Bot

This is a discord bot that provides player statistics for the game Dead by Daylight.

The bot utilizes the [dbd.tricky.lol](https://dbd.tricky.lol/) API as well as the Steam Community API to get player data.
This bot also uses [nightlight.gg](https://nightlight.gg/) as its source for perk icons.

## Commands

The bot currently supports the following commands.
If you have a Vanity Profile URL set on steam, you can use that instead of a Steam ID for any command

`-help` : Displays all available commands

`-stats <steamID>` : Gives general stats about a player, such as player level, rank, playtime, and more

`-survivor <steamID>` : Gives stats about a player's survivor games, such as generators completed, survivors healed, unhooks, and more

`-escapes <steamID>` : Gives more detailed stats about how many times a player has escaped the trial

`-killer <steamID>` : Gives stats about a player's killer games, such ass kills, hatches closed, and more

`-screams <steamID>` : Displays the number of times a player has screamed while playing as survivor

`-randomize <survivor | killer> [# of perks] [-d]` : Gives a random set of 1-4 perks (4 by default) for either survivor or killer. Adding `-d` as an argument adds the perks' full descriptions

## Troubleshooting

For this bot to work, you must have your steam profile set to public. You can set this by going to your Steam Profile > Edit Profile > Privacy Settings and setting "My Profile" and "Game Details" to Public. Wait a few minutes for it to update after doing this.

If you are still having trouble with some commands, try visiting [dbd.tricky.lol](https://dbd.tricky.lol/) and searching with your own SteamID. The site may not have you data yet and it could take some time to load. The bot should work after doing this and waiting a few minutes.

As stated above, you can also use your Vanity Profile URL instead of a Steam ID with these commands. This can be set by going to Edit Profile > General and setting a Custom URL. Whatever you save in that box can be used with the bot.

If you have any other issues, questions, or suggestions, you can contact me through my discord which is natie8. Thank you for reading! :)