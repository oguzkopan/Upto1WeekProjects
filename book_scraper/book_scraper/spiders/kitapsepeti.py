import scrapy
from ..items import BookScraperItem
from scrapy.spiders import CrawlSpider, SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BooksSpiderKitapSepeti(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    name = "kitapsepeti"
    allowed_domains = ["kitapsepeti.com"]
    base_url = "https://www.kitapsepeti.com/cizgi-roman?stock=1&pg=" #change base url according to category you selected

    collection_name = 'kitapsepeti'

    def start_requests(self):
        max_pages = 10  # Set the maximum number of pages you want to scrape
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}{page}"
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # Check if the response is empty or doesn't contain the data you expect
        if not response.body:
            self.logger.warning(f"Page {response.url} returned an empty response. Skipping...")
            return

        # Parse each quote div 
        for book in response.css('div.productDetails.loaderWrapper'):
            item = {}
            self.logger.debug("Direct log statement")
            # Extract title from the link with class "text-description"
            item['title'] = book.css('a.text-description::text').get().strip()
            # Extract publisher from the link with class "text-title mt"
            item['publisher'] = book.css('a.text-title.mt::text').get().strip()
            # Extract model from the link with id "productModelText"
            item['authors'] = book.css('a#productModelText::text').get().strip()
            # Extract price from the div with class "currentPrice"
            item['price'] = book.css('div.currentPrice::text').get().strip()

            yield item  

        # Follow pagination links to continue scraping subsequent pages
        for next_page in response.css('ul.pagination a.next'):
            yield response.follow(next_page, callback=self.parse)