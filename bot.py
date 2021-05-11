# (c) @AbirHasan2005

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from youtubesearchpython import VideosSearch
from helper_func.get_vid_duration import duration
from helper_func.send_audio_file import send_audio
from helper_func.youtube_regex import youtube_link_regex
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InputTextMessageContent, InlineQueryResultArticle

API_ID = (os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

MusicBot = Client(session_name="Music_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@MusicBot.on_message(filters.command("start") & ~filters.edited)
async def start_handler(_, message: Message):
    await message.reply_text(
        text="Hello I am YouTube Music Downloader Bot!",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")],
                [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
                 InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]
            ]
        )
    )


@MusicBot.on_message(filters.regex(youtube_link_regex) & ~filters.edited)
async def youtube_handler(bot: Client, message: Message):
    editable = await message.reply_text(
        text="Trying to Download ...",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    youtube_link = message.text.strip()
    filext = "%(title)s.%(ext)s"
    userdir = os.path.join(os.getcwd(), str(message.from_user.id))
    filepath = os.path.join(userdir, filext)
    command_to_exec = [
        "youtube-dl",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", filepath,
        youtube_link
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    print(t_response)
    try:
        filepath = t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()
    except Exception as err:
        print(f"Can't Get File Name!\nError: {err}")
        try:
            os.remove(filepath)
        except:
            pass
        return
    await editable.edit(
        text="Trying to Upload ..."
    )
    vid_dur = None
    try:
        vid_dur = round(duration(filepath))
        if vid_dur == 400:
            print("Got Error While Trying to Extract Audio Duration!")
            vid_dur = None
        else:
            pass
    except Exception as err:
        print(f"Got Error While Trying to Extract Audio Duration!\nTraceback: {err}")
    try:
        await send_audio(bot, message, filepath, vid_dur)
        await editable.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await send_audio(bot, message, filepath, vid_dur)
        await editable.delete()
    except Exception as error:
        await editable.edit(
            text=f"Unable to Send Audio File!\n\n**Error:** `{error}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]
                ]
            )
        )
    try:
        os.remove(filepath)
    except:
        pass


@MusicBot.on_inline_query()
async def inline_handlers(bot: Client, query: InlineQuery):
    answers = []
    string = query.query.lower().strip().rstrip()

    if string == "":
        await bot.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_parameter="start",
            cache_time=0
        )
        return
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=f"Duration: {v['duration']}, {v['viewCount']['short']}",
                    input_message_content=InputTextMessageContent(
                        "https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_parameter="start",
            )


MusicBot.run()
