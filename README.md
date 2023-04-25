# Compressor-Bot
Telegram bot to convert mkv and mp4 files to h265 mkv
Fill the variables in https://github.com/pachax001/Compressor-Bot/blob/main/docker-compose.yml file.
Fiil the variables in https://github.com/pachax001/Compressor-Bot/blob/main/bot.py file.
Variables need to be filled
API_ID = Get it from here https://my.telegram.org/auth
API_HASH = "" Get it from here https://my.telegram.org/auth
BOT_TOKEN = "" Create a new bot using https://t.me/BotFather
LOG_CHANNEL = "" Create a log channel and add the channel id
OWNER_ID = "" Get it from talking  to https://t.me/MissRose_bot
Bot will work for only owner.
Bot is using ultrafast preset for conversion from ffmpeg.
Use docker compose to host the bot on a vps.
Follow the https://docs.docker.com/engine/install/ubuntu/ to install docker.
After installing clone the repo and fill the variables save files.
Then use 'sudo docker compose up' to start the bot.
Docker image support for linux amd64, arm64/v8, arm/v7
Remember to send /start command in the LOG_CHANNEl also to start the bot to work.
Only one task at a time.
Bot renames the x264 h264 to x265 after conversion.Also if the file doesn't have a codec ot adds .x265 before the extension.If a file is a HDTV file it gets renamed to HDTV.x265.

