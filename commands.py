from telegram.ext import CommandHandler
from datetime import time
import db
import db.operations


def _start(update, context):
    db.operations.addUser(update.effective_user.id, update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, " + update.effective_user.username + ", you have been registered to our platform.\nType /help to learn to use this bot")

def _help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/help shows you this message\n/add <url> adds a feed to your subscriptions\n/setFeedTime <HH:MM> to set your daily feed time\n")

def _add(update, context):
    if (len(context.args) == 1):
        db.operations.addSubscription(update.effective_user.id, context.args[0])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Your rss feed has been added")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Check your format")

def _setFeedTime(update, context):
    newFeedTime = time.fromisoformat(context.args[0])
    db.operations.setFeedTime(update.effective_user.id, newFeedTime)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your new feed time is " + str(newFeedTime.hour) + ":" + str(newFeedTime.minute))

def _debugMagic(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="UID: " + str(update.effective_user.id) + "\nChatID: " + str(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text="*ciccio*", parse_mode='MarkdownV2')

start = CommandHandler('start', _start)
help = CommandHandler('help', _help)
add = CommandHandler('add', _add)
setFeedTime = CommandHandler('setFeedTime', _setFeedTime)
debugMagic = CommandHandler('debugMagic', _debugMagic)