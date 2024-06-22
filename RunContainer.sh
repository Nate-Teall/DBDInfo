docker rmi nateteall/dbd-info
docker build -t nateteall/dbd-info .

docker run -it -d -e DISCORD_TOKEN=$DISCORD_TOKEN -e STEAM_API_KEY=$STEAM_API_KEY --name discord-bot-container nateteall/dbd-info
docker exec -it discord-bot-container sh