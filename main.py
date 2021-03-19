import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


from telegram.ext import Updater, JobQueue
from config import config

updater = Updater(token=config['TOKEN'])
bot = updater.bot
dispatcher = updater.dispatcher

from bot.commands import *
dispatcher.add_handler(start)
dispatcher.add_handler(help)
# dispatcher.add_handler(addRss)
dispatcher.add_handler(addPodcast)
dispatcher.add_handler(forceUpdate)
dispatcher.add_handler(setFeedTime)
dispatcher.add_handler(debugMagic)

updater.start_polling()

# from routines import createRoutine
# import threading
# routine = createRoutine(bot)
#
# threading.Timer(config['UPDATE_FREQ'], routine).start()