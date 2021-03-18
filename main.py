import toml

config = toml.load("config.toml")

from telegram.ext import Updater

updater = Updater(token=config['TOKEN'])
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from commands import *
dispatcher.add_handler(start)
dispatcher.add_handler(help)
dispatcher.add_handler(add)
dispatcher.add_handler(setFeedTime)
dispatcher.add_handler(debugMagic)

updater.start_polling()