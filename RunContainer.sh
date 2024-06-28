docker run -it -d -e DISCORD_TOKEN=$DISCORD_TOKEN -e STEAM_API_KEY=$STEAM_API_KEY --mount type=bind,source="$(pwd)"/,target=/usr/local/DBDInfo --name discord-bot-container nateteall/dbd-info
docker exec -it discord-bot-container sh
