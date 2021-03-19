
# Get users that want their update at that time
# For each user get the Subscriptions
# For each subscription check if it's in dictionary, if it isn't get url from dbStuff and add it, then sendUpdates regardessly

from datetime import datetime, timedelta
from dbStuff.engine import session
from dbStuff import schema
from config import config
from parseandsend import podcasts


def createRoutine(bot):
    def sendUpdates():
        startInt = (datetime.now() - timedelta(minutes=config['UPDATE_FREQ'])).time()
        endInt = datetime.now().time()
        toUpdate = session.query(schema.User).filter(schema.User.FeedTime > startInt, schema.User.FeedTime <= endInt).join(schema.PSubscription).join(schema.Feed).all()
        d = dict()
        for item in toUpdate:
            for sub in item.subscriptions:
                if sub.feed.FID not in d:
                    try:
                        d[sub.feed.FID] = podcasts.PodcastFeed(sub.feed.URL)
                    except:
                        print("An item failed")

                if sub.feed.FID in d:
                    d[sub.feed.FID].sendUpdates(chat_id=item.ChatID, bot=bot, lastUpdate=(datetime.now()-timedelta(days=10)).date())
                    sub.LatestCheck = datetime.today()
                    session.update()

    return sendUpdates