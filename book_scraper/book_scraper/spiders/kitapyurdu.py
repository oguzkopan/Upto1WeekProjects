import scrapy
from ..items import BookScraperItem
from scrapy.spiders import CrawlSpider, SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BooksSpider(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    name = "kitapyurdu"
    allowed_domains = ["kitapyurdu.com"]
    base_url = "https://www.kitapyurdu.com/index.php?route=product/category&filter_category_all=true&path=1&filter_in_stock=1&sort=purchased_365&order=DESC&limit=100&page=" #change base url according to category you selected

    collection_name = 'kitapyurdu'

    def start_requests(self):
        max_pages = 10  # Set the maximum number of pages you want to scrape
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}{page}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Check if the response is empty or doesn't contain the data you expect
        if not response.body:
            self.logger.warning(f"Page {response.url} returned an empty response. Skipping...")
            return

        # Parse each quote div 
        for book in response.css('div.product-cr'):
            item = {}
            item['title'] = book.css('div.name.ellipsis span::text').get()
            # Extract author from the span inside the div with class "author"
            item['authors'] = book.css('div.author span::text').get()
            # Extract publisher from the span inside the div with class "publisher"
            item['publisher'] = book.css('div.publisher span::text').get()
            # Extract price from the span inside the div with class "price-new"
            item['price'] = book.css('div.price-new span.value::text').get()

            yield item  

        # Follow pagination links to continue scraping subsequent pages
        for next_page in response.css('ul.pagination a.next'):
            yield response.follow(next_page, callback=self.parse)
