from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
import datetime
import pytz

from Scrapers import NYTSpider, CNBCSpider, TheGuardianSpider
from ArticleUrlSrapers import NytUrlSpider


def print_(item):
    print(item["time"])


def main():
    crawler = CrawlerProcess()
    dispatcher.connect(print_, signal=signals.item_passed)
    from_stamp = datetime.datetime.fromtimestamp(1628208000).replace(tzinfo=pytz.timezone("GMT"))
    to_stamp = datetime.datetime.now(tz=pytz.timezone("GMT"))
    crawler.crawl(NytUrlSpider, from_stamp, to_stamp, "dEYB91wVRPuecq1hE6VZaoZOZtbKcGh7", subsections_to_include=[
        "Politics", "Europe", "Asia Pacific", "Middle East", "Africa", "Australia", "Americas", "Canada"])
    crawler.start()


def main2():
    from scrapy.selector import Selector
    from scrapy.http import HtmlResponse
    import requests
    from Scrapers import parse_cnbc

    url = "https://www.cnbc.com/2021/08/10/stock-market-news-today.html"

    data = requests.get(url).text

    response = HtmlResponse(url=url, body=data, encoding="utf-8")
    print(parse_cnbc(response, {"time": "wdwd"}))


if __name__ == "__main__":
    main()
