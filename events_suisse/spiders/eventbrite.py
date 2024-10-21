import scrapy


class EventSpider(scrapy.Spider):
    name = 'eventbrite'
    start_urls = ['https://www.eventbrite.fr/d/switzerland/suisse/?page=1']

   
    MAX_PAGES = 5

    def parse(self, response):
        
        events = response.css('section.DiscoverHorizontalEventCard-module__cardWrapper___2_FKN')

        for event in events:
            event_link = event.css('a.event-card-link::attr(href)').get()
            category = event.css('a.event-card-link::attr(data-event-category)').get()
            if event_link:
                
                yield response.follow(event_link, self.parse_event, meta={'category': category})

    
        current_page = int(response.url.split('=')[-1])
        if current_page < self.MAX_PAGES:
            next_page = f'https://www.eventbrite.fr/d/switzerland/suisse/?page={current_page + 1}'
            yield response.follow(next_page, self.parse)

        

    def parse_event(self, response):
        title = response.css('h1.event-title::text').get(default='').strip()
        date = response.css('span.date-info__full-datetime::text').get(default='').strip()
        description = response.css('div.eds-l-mar-vert-6.eds-l-sm-mar-vert-4.eds-text-bm.structured-content-rich-text p::text').getall()
        location = response.css('p.location-info__address-text::text').get(default='').strip()
        image_url = response.css('source[srcset]::attr(srcset)').get(default='')
        category = response.meta.get('category', '')
        price = response.css('div.conversion-bar__panel-info::text').get(default='').strip()
        if not price :
            price = '0'

        yield {
            'title': title,
            'date': date,
            'description': description,
            'price': price,
            'location': location,
           'image_url': image_url,
            'event_link': response.url,
            'category': category,  
        }

       
