from telegram.ext import CommandHandler
from datetime import time, datetime
from dbStuff import schema
from dbStuff.engine import session
from parseandsend import rss, podcasts


def _start(update, context):
    if session.query(schema.User.UID).filter_by(UID=update.effective_user.id).scalar() is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome back, " + update.effective_user.username)
    else:
        newUser = schema.User(UID=update.effective_user.id, ChatID=update.effective_chat.id, FeedTime=time(hour=7, minute=30))
        session.add(newUser)
        session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, " + update.effective_user.username + ", you have been registered to our platform.\nType /help to learn to use this bot")
        print("New user " + update.effective_user.username)


def _help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/help shows you this message\n/addPodcast <url> adds a podcast feed to your subscriptions\n/setFeedTime <HH:MM> to set your daily feed time WIP\n")



# def _addRss(update, context):
#     if (len(context.args) == 1):
#         res = session.query(schema.Feed).filter_by(Type="rss", URL=context.args[0]).first()
#         FID = None
#         if res is None:
#             # Check if the url works
#             feedParsed = None
#             try:
#                 feedParsed = rss.RssFeed(context.args[0])
#                 newFeed = schema.Feed(
#                     Title = feedParsed.title,
#                     URL = context.args[0],
#                     Type = "rss"
#                 )
#                 session.add(newFeed)
#                 session.commit()
#                 FID = newFeed.FID
#             except:
#                 context.bot.send_message(chat_id=update.effective_chat.id, text="There was a problem parsing your rss feed")
#                 return
#         else:
#             FID = res.FID
#             feedParsed = podcasts.PodcastFeed(res.URL)
#
#         feedParsed.sendUpdates(update.effective_chat.id, bot=context.bot)
#         newSubscription = schema.PSubscription(
#             UID = update.effective_user.id,
#             FID = FID,
#             LatestCheck = datetime.now()
#         )
#         session.add(newSubscription)
#         session.commit()
#
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Podcast added")
#
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Check your format")



def _addPodcast(update, context):
    if (len(context.args) == 1):
        res = session.query(schema.PSubscription).filter(schema.PSubscription.UID==update.effective_user.id)\
            .join(schema.Feed).filter(schema.Feed.URL==context.args[0]).first()
        if res is not None:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You have already added this feed to your subscriptions")
            return

        res = session.query(schema.Feed).filter_by(Type="podcast", URL=context.args[0]).first()
        FID = None
        if res is None:
            # Check if the url works
            feedParsed = None
            try:
                feedParsed = podcasts.PodcastFeed(context.args[0])
                newFeed = schema.Feed(
                    Title = feedParsed.title,
                    URL = context.args[0],
                    Type = "podcast"
                )
                session.add(newFeed)
                session.commit()
                FID = newFeed.FID
            except:
                context.bot.send_message(chat_id=update.effective_chat.id, text="There was a problem parsing your url")
                return
        else:
            FID = res.FID
            feedParsed = podcasts.PodcastFeed(res.URL)

        feedParsed.sendUpdates(update.effective_chat.id, bot=context.bot)
        newSubscription = schema.PSubscription(
            UID = update.effective_user.id,
            FID = FID,
            LatestCheck = datetime.today()
        )
        session.add(newSubscription)
        session.commit()

        context.bot.send_message(chat_id=update.effective_chat.id, text="Podcast added")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Check your format")


def _forceUpdate(update, context):
    q = session.query(schema.PSubscription).filter(schema.PSubscription.UID == update.effective_user.id).join(schema.Feed).all()
    for item in q:
        curr = podcasts.PodcastFeed(item.feed.URL)
        curr.sendUpdates(update.effective_chat.id, context.bot, item.LatestCheck)




def _setFeedTime(update, context):
    newFeedTime = time.fromisoformat(context.args[0])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your new feed time is " + str(newFeedTime.hour) + ":" + str(newFeedTime.minute))

def _debugMagic(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="UID: " + str(update.effective_user.id) + "\nChatID: " + str(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text="*ciccio*", parse_mode='MarkdownV2')

start       = CommandHandler('start', _start)
help        = CommandHandler('help', _help)
# addRss      = CommandHandler('addRss', _addRss)
addPodcast  = CommandHandler('addPodcast', _addPodcast)
forceUpdate = CommandHandler('forceUpdate', _forceUpdate)
setFeedTime = CommandHandler('setFeedTime', _setFeedTime)
debugMagic  = CommandHandler('debugMagic', _debugMagic)
