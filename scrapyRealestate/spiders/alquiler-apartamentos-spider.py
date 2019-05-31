import scrapy
import csv
BASE_URL = "https://www.encuentra24.com"
URL = "/panama-es/bienes-raices-alquiler-apartamentos.%d"

class QuotesSpider(scrapy.Spider):
    name = "alquiler_apartamentos"
    start_urls = (BASE_URL + URL) % 1
    filename = 'venta-de-apartamentos.csv'
    
    # def __init__(self):
    #     self.page_number = 1  
    def start_requests(self):
        print(self.start_urls)
        self.page_number = 1
        
        # row = ["propietario", "telefono", "categoria", "localizacion", "precio", "metros", "recamaras", "banos", "url"]
        # with open(self.filename, mode='a', encoding='utf-8') as csvFile:
        #     writer = csv.writer(csvFile)
        #     writer.writerow(row)
        # csvFile.close()           
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
            #link = article.xpath('//a[@class="more-details"]/@href').extract()
            link = article.css('a.more-details::attr(href)').get()
            print(link)
            absolute_url = BASE_URL + link
            yield scrapy.Request(url=absolute_url, callback=self.parse_listing)
            # price = article.css("div.ann-box-details span.ann-price::text").get()
            # if isinstance(price, str):
            #     price = price.strip()   
            # title = article.css("div.ann-box-details a span::text").get()
            # if title is None:
            #     title = article.css("div.ann-box-details a strong::text").get()
            # title = str(title)
            # if isinstance(title, str):
            #     title = title.strip()            
            # desc = article.css("div.ann-box-details span.ann-box-desc::text").get()
            # if isinstance(desc, str):
            #     desc = desc.strip()
            #     desc = desc.replace('\n', ' ')
            # info = article.css("div.ann-box-details span.ann-info-item::text").extract()[-1]
            # if isinstance(info, str):
            #     info = info.strip()
            # companyName = article.css("div.ann-box-contact span.company-name::text").extract()
            # if isinstance(companyName, list):
            #     companyName = ' '.join(companyName)
            # if isinstance(companyName, str):
            #     companyName = companyName.replace('\n', ' ')
            #     companyName = companyName.strip()
            # phone = article.css("div.ann-box-contact span.phone::text").extract()
            # print(phone)
            # if not phone:
            #     phone = ''
            # else:
            #     if isinstance(phone, list):
            #         if len(phone) > 1:
            #             phone = phone[1]
            #         else:
            #             phone = phone[0]
            #     if isinstance(phone, str):
            #         phone = phone.strip()
            # filename = 'venta-de-apartamentos.csv'
            # row = [title, desc, price, info, companyName, phone]
            # with open(filename, mode='a', encoding='utf-8') as csvFile:
            #     writer = csv.writer(csvFile)
            #     writer.writerow(row)
            # csvFile.close()

            #yield 'Saved file %s' % filename
        self.page_number += 1
        yield scrapy.Request(url=(BASE_URL + URL) % self.page_number, callback=self.parse)

    def parse_listing(self, response):
    #info = response.css('div.ad-info')
    #categoria: info.xpath('//span[contains(@class, "info-name") and contains(text(), "Categoria:")]/following-sibling::span/text()').get()
    #localizacion: info.xpath('//span[contains(@class, "info-name") and contains(text(), "Localización:")]/following-sibling::span/text()').get()

    #details = response.css('div.ad-details')
    #recamaras = details.xpath('//span[contains(@class, "info-name") and contains(text(), "Recámaras:")]/following-sibling::span/text()').get()
    #banos = details.xpath('//span[contains(@class, "info-name") and contains(text(), "Baños:")]/following-sibling::span/text()').get()
    #metros = details.xpath('//span[contains(@class, "info-name") and re:test(text(),"^M² de construcción:$")]/following-sibling::span/text()').get()

    #propietario: response.xpath('//div[contains(@class,"user-info")]/a/span[contains(@class,"user-name")]/text()').get()
    #telefono: response.xpath('//div[contains(@class,"contact-phone")]/span[contains(@class,"phone")]/text()').get()
        tipo = response.xpath('//div[contains(@class,"user-info")]/span[contains(@class,"text-attr")]/text()').get()
        if tipo == "Propietario":
            info = response.css('div.ad-info')
            categoria = info.xpath('//span[contains(@class, "info-name") and contains(text(), "Categoria:")]/following-sibling::span/text()').get()
            localizacion = info.xpath('//span[contains(@class, "info-name") and contains(text(), "Localización:")]/following-sibling::span/text()').get()
            precio = info.xpath('//span[contains(@class, "info-name") and contains(text(), "Precio:")]/following-sibling::span/text()').get()
            details = response.css('div.ad-details')
            recamaras = details.xpath('//span[contains(@class, "info-name") and contains(text(), "Recámaras:")]/following-sibling::span/text()').get()
            banos = details.xpath('//span[contains(@class, "info-name") and contains(text(), "Baños:")]/following-sibling::span/text()').get()
            metros = details.xpath('//span[contains(@class, "info-name") and re:test(text(),"^M² de construcción:$")]/following-sibling::span/text()').get()
            propietario = response.xpath('//div[contains(@class,"user-info")]/span[contains(@class,"user-name")]/text()').get()
            if not propietario:
                propietario = response.xpath('//div[contains(@class,"user-info")]/a/span[contains(@class,"user-name")]/text()').get()
            telefono= response.xpath('//div[contains(@class,"contact-phone")]/span[contains(@class,"phone")]/text()').get()        
            #row = [propietario, telefono, categoria, localizacion, precio, metros, recamaras, banos, response.url]
            return {"propietario": propietario, "telefono": telefono, "categoria": categoria, "localizacion": localizacion, "precio": precio, "metros": metros, "recamaras": recamaras, "banos":banos, "url":response.url}
            # print(row)
            # with open(self.filename, mode='a', encoding='utf-8') as csvFile:
            #     writer = csv.writer(csvFile)
            #     writer.writerow(row)
            # csvFile.close()        