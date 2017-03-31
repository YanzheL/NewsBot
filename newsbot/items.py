from scrapy.item import Item, Field


class Website(Item):
    author = Field()
    title = Field()
    article = Field()
    description = Field()
    url = Field()
    date = Field()
    topic = Field()
