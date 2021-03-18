import podcastparser
from urllib.request import urlopen
from datetime import date

from parseandsend._article import Article, Feed

class PodcastArticle(Article):
    def send(self, ChatID, bot):
        messageContent = "*" + self.title + "*\n" + self.description + "\n"
        bot.sendMessage(chat_id=ChatID, text=messageContent, parse_mode='html')
        if (self.link != ''):
            bot.sendMessage(chat_id=ChatID, text="Link: " + self.link)


class PodcastFeed(Feed):
    def __init__(self, link):
        super().__init__()
        feed = podcastparser.parse(link, urlopen(link))
        self.title = feed['title']
        for item in feed['episodes']:
            self.items.append(PodcastArticle(item['title'], item['description'], item['link'], date.fromtimestamp(item['published'])))
        self.items.reverse()