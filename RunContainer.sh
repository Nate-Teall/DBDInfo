docker rmi nateteall/dbd-info
docker build -t nateteall/dbd-info .

docker run --rm -it -d -e DISCORD_TOKEN=$DISCORD_TOKEN --name discord-bot-container nateteall/dbd-info
docker exec -it discord-bot-container sh