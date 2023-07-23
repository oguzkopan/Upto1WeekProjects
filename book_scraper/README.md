You can fetch data from 'kitapsepeti.com' with this command after going into book_scraper directory:

scrapy crawl kitapsepeti

You can fetch data from 'kitapyurdu.com' with this command after going into book_scraper directory:

scrapy crawl kitapyurdu

You can change these variables from spider/ path:

max_pages = 10  # Set the maximum number of pages you want to scrape
base_url = "https://www.kitapsepeti.com/cizgi-roman?stock=1&pg="  #change base url according to category you selected