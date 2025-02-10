# Scrapy settings for monprojet project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "monprojet"

SPIDER_MODULES = ["monprojet.spiders"]
NEWSPIDER_MODULE = "monprojet.spiders"

# Respecte les règles de robots.txt
ROBOTSTXT_OBEY = True

# Activation du pipeline
ITEM_PIPELINES = {
    "monprojet.pipelines.MongoDBPipeline": 300,
}

# Configuration MongoDB
MONGO_URI = "mongodb://localhost:27017/?socketTimeoutMS=60000&connectTimeoutMS=60000"
MONGO_DATABASE = "f1_data"

# User agent pour éviter le blocage
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Pause entre les requêtes pour éviter de surcharger le serveur
DOWNLOAD_DELAY = 2

DOWNLOADER_MIDDLEWARES = {
    'monprojet.middlewares.RandomUserAgentMiddleware': 400,
}

ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
