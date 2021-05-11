# (c) @AbirHasan2005

import os


async def send_audio(bot, message, filepath, vid_dur):
    await bot.send_audio(
        chat_id=message.chat.id,
        audio=filepath,
        caption=f"{os.path.basename(filepath)}",
        duration=vid_dur
    )
