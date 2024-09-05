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

For this bot to work