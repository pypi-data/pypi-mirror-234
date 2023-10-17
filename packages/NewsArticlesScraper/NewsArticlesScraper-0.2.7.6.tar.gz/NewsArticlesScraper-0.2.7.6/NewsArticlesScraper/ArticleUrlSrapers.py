import scrapy
import ciso8601
import datetime
import logging
import pytz


class CnbcUrlSpider(scrapy.Spider):
    """Spider to scrape CNBC article urls.

    """
    name = 'CnbcUrlSpider'

    allowed_domains = ["api.queryly.com"]
    start_urls = []
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        # 'JOBDIR': './News/CNBCJobs',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
        'DOWNLOAD_DELAY': 0.5,
        'RANDOM_UA_TYPE': "random",
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
    }

    def __init__(self, from_time: datetime.datetime, until_time: datetime.datetime, user_agent=None,
                 query: str = "cnbc", **kwargs):
        self.url_stream = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query=" + \
                          query + "&endindex={" \
                                  "}&batchsize=100&timezoneoffset=-60&sort=date"
        self.from_time = from_time
        self.until_time = until_time
        self.start_page = None
        self.end_page = None
        if user_agent is not None:
            self.custom_settings["USER_AGENT"] = user_agent
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url_stream.format(0), callback=self.get_total_pages)

    def get_total_pages(self, response):
        data = response.json()
        metadata = data["metadata"]
        total_pages = metadata["totalpage"]
        self.start_page = total_pages
        self.end_page = 1
        middle = round(total_pages / 2)
        yield scrapy.Request(self.url_stream.format((middle - 1) * 100), callback=self.locate_start_page)

    def locate_start_page(self, response):
        data = response.json()
        current_page = data["metadata"]["pagerequested"]
        if current_page != 1:
            newest_date = ciso8601.parse_datetime(data["results"][0]["datePublished"])
            oldest_date = ciso8601.parse_datetime(data["results"][-1]["datePublished"])
            if newest_date <= self.from_time:
                middle = round((current_page + self.end_page) / 2)
                self.start_page = current_page
                yield scrapy.Request(self.url_stream.format((middle - 1) * 100) + "&x=1",
                                     callback=self.locate_start_page)
            if newest_date > self.from_time:
                if oldest_date < self.from_time:
                    logging.info(f"Found start page: {current_page}")
                    yield scrapy.Request(response.url + "&x=1", callback=self.parse)
                    # + "&x=1" is needed because scrapy won't request same page twice
                else:
                    middle = round((current_page + self.start_page) / 2)
                    self.end_page = current_page
                    yield scrapy.Request(self.url_stream.format((middle - 1) * 100) + "&x=1",
                                         callback=self.locate_start_page)

    def parse(self, response, **kwargs):
        data = response.json()
        metadata = data["metadata"]
        current_page = metadata["pagerequested"]
        logging.info(f"Requested page {current_page}")

        if current_page:
            if current_page > 1:
                page = (current_page - 2) * 100
                yield scrapy.Request(
                    url=self.url_stream.format(page),
                    callback=self.parse)
        else:
            logging.error(f"Current page not found when requesting {response.url}.")

        for result in data["results"]:
            t = ciso8601.parse_datetime(result["datePublished"])
            if self.from_time < t < self.until_time:
                premium = False
                if "cn:contentClassification" in result:
                    clasf = result["cn:contentClassification"]
                    if "premium" in clasf:
                        premium = True
                if not premium:
                    if result["cn:branding"] == "cnbc":
                        if result["cn:type"] not in ["cnbcvideo", "live_story"]:
                            yield {"url": result["cn:liveURL"],
                                   "time": t,
                                   "origin": "c"}


class NytUrlSpider(scrapy.Spider):
    """Spider to scrape NYT article urls.

    """
    name = 'NytUrlSpider'
    allowed_domains = ['api.nytimes.com']
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 12,
        # 'JOBDIR': './News/NYTJobs',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'DOWNLOAD_TIMEOUT': 1200,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
        'RANDOM_UA_TYPE': "random",
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
    }

    def __init__(self, from_time: datetime.datetime, until_time: datetime.datetime, api_key, user_agent=None,
                 subsections_to_include: list = None, **kwargs):
        self.api_key = api_key
        self.from_time = from_time
        self.until_time = until_time
        if (datetime.datetime.now(pytz.timezone("GMT")) - self.until_time).total_seconds() <= 86400:
            self.recent = True
        else:
            self.recent = False
        if user_agent is not None:
            self.custom_settings["USER_AGENT"] = user_agent
        self.subsections_to_include = subsections_to_include
        super().__init__(**kwargs)

    def start_requests(self):
        url_api_historic = "https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key=" + self.api_key
        year_min = int(self.from_time.strftime('%Y'))
        month_min = int(self.from_time.strftime('%m'))
        year_max = int(self.until_time.strftime('%Y'))
        month_max = int(self.until_time.strftime('%m'))

        for month in range(month_min, 13):
            yield scrapy.Request(url_api_historic.format(year_min, month),
                                 callback=self.parse, meta={"api_point": "historic"})

        for year in range(year_min + 1, year_max):
            for month in range(1, 13):
                yield scrapy.Request(url_api_historic.format(year, month),
                                     callback=self.parse, meta={"api_point": "historic"})
        for _month in range(1, month_max + 1):
            yield scrapy.Request(url_api_historic.format(year_max, _month),
                                 callback=self.parse, meta={"api_point": "historic"})
        if self.recent:
            url_api_recent = f"https://api.nytimes.com/svc/news/v3/content/all/world.json?api-key={self.api_key}" \
                             f"&limit=500"
            yield scrapy.Request(url_api_recent, callback=self.parse, meta={"api_point": "recent"})

    def parse(self, response, **kwargs):
        data = response.json()
        api_point = response.meta["api_point"]
        if api_point == "historic":
            articles = data["response"]["docs"]
        else:
            articles = data["results"]
        for article in articles:
            if api_point == "historic" and self.subsections_to_include is not None:
                subsection = article.get("subsection_name", None)
                if subsection is None:
                    continue
                if subsection not in self.subsections_to_include:
                    continue
            if api_point == "recent" and self.subsections_to_include is not None:
                if article["subsection"] not in self.subsections_to_include:
                    continue
            if api_point == "historic":
                pub_date = article["pub_date"]
            else:
                pub_date = article["published_date"]
            pub_date = ciso8601.parse_datetime(pub_date)
            if pub_date < self.from_time:
                break
            if pub_date > self.until_time:
                break
            if api_point == "historic":
                url = article["web_url"]
            else:
                try:
                    url = article["related_urls"][0]["url"]
                except (TypeError, IndexError):
                    url = article["url"]
            yield {"url": url,
                   "time": pub_date,
                   "origin": "n"}


class TheGuardianSpider(scrapy.Spider):
    """Spider to scrape The Guardian article urls.

    """
    name = 'TheGuardianSpider'
    allowed_domains = ['content.guardianapis.com']
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 6,
        # 'JOBDIR': './News/TheGuardianJobs',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'DOWNLOAD_TIMEOUT': 300,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
        'RANDOM_UA_TYPE': "random",
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
    }

    def __init__(self, from_time: datetime.datetime, until_time: datetime.datetime, api_key="test", user_agent=None,
                 **kwargs):
        self.api_key = api_key
        self.from_time = from_time
        self.until_time = until_time
        self.url = f"https://content.guardianapis.com/world?api-key={self.api_key}" \
                   f"&page-size=200&use-date=first-publication" \
                   f"&from-date={self.from_time.strftime('%Y-%m-%d')}" \
                   f"&to-date={self.until_time.strftime('%Y-%m-%d')}&page="
        if user_agent is not None:
            self.custom_settings["USER_AGENT"] = user_agent
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url + "1",
                             callback=self.paginate)

    def paginate(self, response):
        data = response.json()["response"]
        max_pages = data["pages"]
        for page_number in range(1, max_pages + 1):
            to_request_url = self.url + str(page_number) + "&x=1"
            yield scrapy.Request(to_request_url, callback=self.parse_api)

    @staticmethod
    def parse_api(response):
        data = response.json()["response"]
        articles = data["results"]
        for article in articles:
            yield {"url": article["webUrl"],
                   "time": ciso8601.parse_datetime(article["webPublicationDate"]),
                   "origin": "g"}
