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

TOKEN = '5128554563:AAGXrWFZ8YKt0lSbFpr6X1xo4P14X-L5NjE'

def start(update: Update, context: CallbackContext):
    """Sends description about bot
    """
    update.message.reply_text('hi')

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
    yt.download()
    query.answer('done')


# handlers here
updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.entity('url'), url))
dp.add_handler(CallbackQueryHandler(url_inline_button))

updater.start_polling()
updater.idle()