import asyncio
from pyrogram import Client, filters
import subprocess
import glob
import psutil
import pyrogram
import os
API_ID = 
API_HASH = ""
BOT_TOKEN = ""
LOG_CHANNEL = ""
OWNER_ID = 
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
ongoing_task = False

@app.on_message(
    filters.command("start") & (filters.user(OWNER_ID) | filters.chat(LOG_CHANNEL))
)
async def start(client, message):
    if message.chat.type == "CHANNEL":
        await app.send_message(chat_id=LOG_CHANNEL, text="Bot is ready!")
    else:
        await app.send_message(
            chat_id=message.chat.id,
            text="Send me a video file",
        )
if not os.path.exists("downloads"):
    os.makedirs("downloads")

@app.on_message(filters.video | filters.document & filters.user(OWNER_ID))
async def converter(client, message):
    global ongoing_task
    if ongoing_task:
        await message.reply_text(
            "A task is already ongoing. Please wait for it to complete before starting a new one."
        )
        return
    ongoing_task = True
    file_id = message.document.file_id if message.document else message.video.file_id
    file_name = message.document.file_name if message.document else message.video.file_name
    username = message.from_user.username
    name = message.from_user.first_name
    id = message.from_user.id
    if file_name.endswith((".mp4", "mkv")) and any(x in file_name for x in ["x265", "X265", "HEVC", "hevc"]):
        await app.send_message(chat_id=message.chat.id,text="Already in HEVC Format",)
    elif file_name.endswith((".mp4", ".mkv")) and message.video is not None:
        try:
            await app.send_video(
            chat_id=LOG_CHANNEL,
            video=file_id,
            caption=f"{file_name}\n\n<b>#cc</b>: @{username} (<code>{name}</code> (<code>{id}</code>))",
        )
            await message.reply_text (f"Successfully forwarded {file_name} to log channel")
        except Exception as e:
            await message.reply_text (f"Cannot Forward {file_name} to Log Channel.Make sure to send /start command in the log channel" +str(e))
        
        try:
            download_message=await message.reply_text("starting download...")
            async def progress(current, total):
                mb_current = current / 1000000
                mb_total = total / 1000000
                print(f"{current * 100 / total:.1f}%")
                percent = current * 100 / total
                await download_message.edit_text(f"Downloaded {mb_current} out of {mb_total} MB ({percent:.1f}%)")
            await message.download(file_name, progress=progress)
            print("File downloaded successfully")
            await download_message.edit_text("Download Complete")
        except Exception as e:
            await download_message.edit_text("Error downloading file... " +str(e))
            ongoing_task=False
            print("Error in download media:", e)
            return
       
    elif file_name.endswith((".mp4", ".mkv")) and message.document is not None:
        try:
            await app.send_document(
            chat_id=LOG_CHANNEL,
            document=file_id,
            caption=f"{file_name}\n\n<b>#cc</b>: @{username} (<code>{name}</code> (<code>{id}</code>))",
        )
            await message.reply_text(f"Successfully forwarded {file_name} to log channel")
        except Exception as e:
            await message.reply_text(f"Cannot Forward {file_name} to Log Channel.Make sure to send /start command in the log channel" +str(e))
            
        try:
           download_message=await message.reply_text("starting download...")
           async def progress(current, total):
                mb_current = current / 1000000
                mb_total = total / 1000000
                print(f"{current * 100 / total:.1f}%")
                percent = current * 100 / total
                await download_message.edit_text(f"Downloaded {mb_current} out of {mb_total} MB ({percent:.1f}%)")
           await message.download(file_name, progress=progress)
           print("File downloaded successfully")
           await download_message.edit_text("Download Complete")
        except Exception as e:
            await download_message.edit_text("Error downloading file... " +str(e))
            ongoing_task=False
            print("Error in download media:", e)
            return
    
    os.chdir("downloads")
    for file in glob.glob("*"):
        ext = os.path.splitext(file)[1].lower()
        if ext == ".mkv" or ext == ".MKV" or ext == ".mp4" or ext == ".MP4":
            if "HDTV.x264" in file:
                new_file = file.replace("HDTV.x264", "HDTV.x265")
            elif any(x in file for x in ["x264", "h264", "X264", "H264", "hdtv", "Hdtv", "HDTV", "hdt"]):
                new_file = (
                    file.replace("x264", "x265")
                    .replace("h264", "x265")
                    .replace("X264", "x265")
                    .replace("H264", "x265")
                    .replace("hdtv", "HDTV.x265")
                    .replace("Hdtv", "HDTV.x265")
                    .replace("HDTV", "HDTV.x265")
                    .replace("hdt", "HDTV.x265")
                )
            else:
                new_file = os.path.splitext(file)[0] + ".x265.mkv"
            convert_message=await message.reply_text("Converting....")
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    file,
                    "-c:v",
                    "libx265",
                    "-preset",
                    "ultrafast",
                    "-c:a",
                    "copy",
                    new_file,
                ]
            )
            await convert_message.edit_text("Conversion Completed")
            upload_message=await message.reply_text("Uploading...")
            async def progress(current, total):
                mb_current = current / 1000000
                mb_total = total / 1000000
                print(f"{current * 100 / total:.1f}%")
                percent = current * 100 / total
                await upload_message.edit_text(f"Uploaded {mb_current} out of {mb_total} MB ({percent:.1f}%)")
            await app.send_video(
                chat_id=message.chat.id, video=new_file, caption=f"{new_file}", progress=progress,
            )
            await app.send_video(
                chat_id=LOG_CHANNEL,
                video=new_file,
                caption=f"{new_file}\n\n<b>#cc</b>: @{username} (<code>{name}</code> (<code>{id}</code>))",
            )
            try:
                os.remove(new_file)
                os.remove(file)
                await message.reply_text("Upload complete! Converted  and Original Files deleted.")
            except OSError:
                await message.reply_text("Upload complete! Unable to delete file.")
    ongoing_task = False  
    
app.run()
