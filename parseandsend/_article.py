class Article:
    def __init__(self, title, description, link, pub_date):
        self.title = title
        self.description = description
        self.link = link
        self.pub_date = pub_date

    def send(self, bot, ChatID):
        print("You should implement this method yourself")

class Feed:
    def __init__(self):
        self.items = list()

    def sendUpdates(self, bot, ChatID, lastUpdate):
        count = 0
        toBeSent = filter(lambda item: item.lastUpdate > lastUpdate, self.items)
        if len(toBeSent)>0:
            bot.sendMessage(chat_id=ChatID, text="*"+self.title+"*", parse_mode='MarkdownV2')
        for item in toBeSent:
            item.send(bot, ChatID)