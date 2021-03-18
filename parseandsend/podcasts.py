import podcastparser
from urllib.request import urlopen
from _article import Article, Feed
from datetime import date

class PodcastArticle(Article):
    def send(self, bot, ChatID):
        messageContent = "*" + self.title + "*\n" + self.description + "\n"
        bot.sendMessage(chat_id=ChatID, text=messageContent, parse_mode='MarkdownV2')
        bot.sendAudio(chat_id=ChatID, audio=self.link)


class PodcastFeed(Feed):
    def __init__(self, link):
        super().__init__()
        feed = podcastparser.parse(link, urlopen(link))
        self.title = feed['title']
        for item in feed['episodes']:
            self.items.append(PodcastArticle(item['title'], item['description'], item['link'], date.fromtimestamp(item['published'])))

