from telegram.ext import (
    Updater, 
    MessageHandler, 
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from pytube import YouTube, Playlist
import os
from env import env

TOKEN = env.get("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    """Sends description about bot
    """
    update.message.reply_text('''<b>Hi this bot helps you for downloading videos from <a href="https://www.youtube.com">YouTue</a>

How to use: /help

Made by @codeschooluz
    </b>''', parse_mode="HTML")

def url(update: Update, context: CallbackContext):
    """ Gets url and sends message about url
    and resolution inline buttons
    """
    text = update.message.text
    yt = YouTube(text)
    streams = yt.streams.filter(progressive=True)

    resolutions = []
    for stream in streams:
        resolutions.append(InlineKeyboardButton(stream.resolution, callback_data=stream.resolution))
    
    reply = InlineKeyboardMarkup([
        [i for i in resolutions[:3]]
    ])
    
    update.message.reply_text(text, reply_markup=reply)

def url_inline_button(update: Update, context: CallbackContext):
    """ When inline button pressed send downloads video with user asked resolution
    and sends video to user also save vidoe id to use other user ask same url video
    """
    query = update.callback_query
    text = query.message.text
    yt = YouTube(text).streams.get_by_resolution(query.data)
    yt.download('videos', 'video.mp4')

    bot = context.bot
    chat_id = update.callback_query.message.chat.id

    #opening video
    f = open('videos/video.mp4', 'rb')
    #sending video to user
    bot.send_video(chat_id, f)
    f.close()
    #deleting video from server
    os.remove('videos/video.mp4')

def help(update: Update, context: CallbackContext):
    update.message.reply_text('''
<b>Send me any YouTube video link,
Choose video quality
And enjoy it 🥳.</b>

<i>Connect with us: @SANJARBEK1718</i>
    ''', parse_mode="HTML")

# # handlers here
# updater = Updater(TOKEN, base_url='http://127.0.0.1:8081/bot')
# # updater.bot.log_out()
# dp = updater.dispatcher

updater = Updater(token=TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('help', help))
dp.add_handler(MessageHandler(Filters.entity('url'), url))
dp.add_handler(CallbackQueryHandler(url_inline_button))