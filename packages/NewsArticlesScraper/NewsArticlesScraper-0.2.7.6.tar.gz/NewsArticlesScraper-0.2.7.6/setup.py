from setuptools import setup, find_packages

VERSION = '0.2.7.6'
DESCRIPTION = 'Scraping news articles'
LONG_DESCRIPTION = 'A package that allows you to scrape news articles from various news sites via scrapy.'

# Setting up
setup(
    name="NewsArticlesScraper",
    version=VERSION,
    author="PySlayer (Paul Antweiler)",
    author_email="antweiler.paul@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['scrapy', 'ciso8601', 'pytz', "scrapy-user-agents"],
    keywords=['python', 'news', 'scraping', 'news scraping', 'news articles'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
