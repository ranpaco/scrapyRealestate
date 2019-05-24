import scrapy
import csv

URL = "https://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos.%d"

class QuotesSpider(scrapy.Spider):
    name = "venta_apartamentos"
    start_urls = URL % 1
    
    # def __init__(self):
    #     self.page_number = 1  
    def start_requests(self):
        print(self.start_urls)
        self.page_number = 1
        yield scrapy.Request(url=self.start_urls, callback=self.parse)
    # def start_requests(self):
    #     urls = [
    #         'https://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos',
    #         'https://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos.2',
    #         'https://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos.3',
    #         'https://www.encuentra24.com/panama-es/bienes-raices-venta-de-propiedades-apartamentos.4',

    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        print (self.page_number)
        print ("----------")
        articles = response.css('article')
        if not articles:
            raise CloseSpider('No more pages')
        for article in articles:    
            price = article.css("div.ann-box-details span.ann-price::text").get()
            if isinstance(price, str):
                price = price.strip()
            title = article.css("div.ann-box-details a span::text").get()
            if title is None:
                title = article.css("div.ann-box-details a strong::text").get()
            title = str(title)
            if isinstance(title, str):
                title = title.strip()            
            desc = article.css("div.ann-box-details span.ann-box-desc::text").get()
            if isinstance(desc, str):
                desc = desc.strip()
                desc = desc.replace('\n', ' ')
            info = article.css("div.ann-box-details span.ann-info-item::text").extract()[-1]
            if isinstance(info, str):
                info = info.strip()
            companyName = article.css("div.ann-box-contact span.company-name::text").extract()
            if isinstance(companyName, list):
                companyName = ' '.join(companyName)
            if isinstance(companyName, str):
                companyName = companyName.replace('\n', ' ')
                companyName = companyName.strip()
            phone = article.css("div.ann-box-contact span.phone::text").extract()
            print(phone)
            if not phone:
                phone = ''
            else:
                if isinstance(phone, list):
                    if len(phone) > 1:
                        phone = phone[1]
                    else:
                        phone = phone[0]
                if isinstance(phone, str):
                    phone = phone.strip()
            #page = response.url.split(".")[-2]
            filename = 'venta-de-apartamentos.csv'
            row = [title, desc, price, info, companyName, phone]
            #row = [title]
            with open(filename, mode='a', encoding='utf-8') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            #yield 'Saved file %s' % filename
        self.page_number += 1
        yield scrapy.Request(url=URL % self.page_number, callback=self.parse)
