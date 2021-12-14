def parse(self, response):
        all_books = response.xpath('//article[@class="product_pod"]')
        for book in all_books:
            book_url = self.start_urls[0] + \
                book.xpath('.//h3/a/@href').extract_first()
            yield scrapy.Request(book_url, callback=self.parse_book)


        next_page_partial_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)