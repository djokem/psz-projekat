import scrapy


class NekretnineSpider(scrapy.Spider):
    name = "nekretnine"

    start_urls = [
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/lista/po-stranici/',
        'https://www.nekretnine.rs/stambeni-objekti/kuce/lista/po-stranici/'
    ]       

    def dev(self, response):

        tip_nekretnine = 'Kuća' if 'kuce' in response.url.split('/')[-4] else 'Stan'
        tip_ponude = '' # u detaljima
        cena = response.css('.stickyBox__price::text').get()
        grad = response.css('.property__location > ul:nth-child(1) > li:nth-child(3)::text').get() 
        deo_grada = response.css('.property__location > ul:nth-child(1) > li:nth-child(4)::text').get()
        kvadratura = '' # u detaljima
        godina_izgradnje = '' # u detaljima
        povrsina_zemljista = '' # samo za kuce # u detaljimaa 
        spratnost = '' if 'Kuća' in tip_nekretnine else response.css('.property__main-details > ul:nth-child(1) > li:nth-child(5) > span:nth-child(2)::text').get().split('/')[1].strip() # samo za stanove # u detaljima
        sprat = '' if 'Kuća' in tip_nekretnine else response.css('.property__main-details > ul:nth-child(1) > li:nth-child(5) > span:nth-child(2)::text').get().split('/')[0].strip()
        uknjizenost = 'Ne' # u detaljima
        tip_grejanja = response.css('.property__main-details > ul:nth-child(1) > li:nth-child(3) > span:nth-child(2)::text').get().strip() 
        ukupan_broj_soba = '' # u detaljima
        ukupan_broj_kupatila = '1' # u detaljima
        parking = response.css('.property__main-details > ul:nth-child(1) > li:nth-child(4) > span:nth-child(2)::text').get().strip()
        stanje_nekretnine = '' # u detaljima


        # Podaci o nekretnini
        i = 1
        li_selector_tag = f'div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child({i})'
        li_selector = f'div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child({i}) > strong:nth-child(1)'

        while response.css(li_selector_tag).get() is not None:
            detail_tag = response.css(li_selector_tag+'::text').get()
            detail = response.css(li_selector+'::text').get().strip()
            # print(li_selector_tag)
            if 'Transakcija' in detail_tag:
                tip_ponude = detail
            elif 'Kvadratura' in detail_tag:
                kvadratura = detail
            elif 'Godina izgradnje' in detail_tag:
                godina_izgradnje = detail
            elif 'Površina zemljišta' in detail_tag:
                povrsina_zemljista = detail
            elif 'Ukupan broj soba' in detail_tag:
                ukupan_broj_soba = detail
            # elif 'Ukupan brој spratova' in detail_tag:
                # spratnost = detail
            elif 'Uknjiženo' in detail_tag:
                uknjizenost = detail
            elif 'Stanje nekretnine' in detail_tag:
                stanje_nekretnine = detail
            elif 'Broj kupatila' in detail_tag:
                ukupan_broj_kupatila = detail

            i += 1
            li_selector_tag = f'div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child({i})'
            li_selector = f'div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child({i}) > strong:nth-child(1)'


        yield {
            'tip_nekretnine' : tip_nekretnine,
            'tip_ponude' : tip_ponude,
            'cena' : cena,
            'grad' : grad,
            'deo_grada' : deo_grada,
            'kvadratura' : kvadratura,
            'godina_izgradnje' : godina_izgradnje,
            'povrsina_zemljista' : povrsina_zemljista,
            'spratnost' : spratnost,
            'sprat' : sprat,
            'uknjizenost' : uknjizenost,
            'tip_grejanja' : tip_grejanja,
            'ukupan_broj_soba' : ukupan_broj_soba,
            'ukupan_broj_kupatila' : ukupan_broj_kupatila,
            'parking' : parking,
            'stanje_nekretnine' : stanje_nekretnine
        }


    def parse_house_rent(self, response):

        broj_kupatila_tag = response.css('div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child(6)::text').get()
        broj_kupatila = response.css('div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child(6) > strong:nth-child(1)::text').get().strip() if 'kupat' in broj_kupatila_tag else '-'

        parking_tag = response.css('.property__main-details > ul:nth-child(1) > li:nth-child(4) > span:nth-child(2) > span:nth-child(1)::text').get()
        parking = response.css('.property__main-details > ul:nth-child(1) > li:nth-child(4) > span:nth-child(2)::text').get().strip() if 'Parking' in parking_tag else '-'

        stanje_nekretnine_tag = response.css('div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child(4)::text').get()
        godina_izgradnje = response.css('div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child(4) > strong:nth-child(1)::text').get().strip() if 'Stanje' in stanje_nekretnine_tag else '-'

        kvadratura_tag = response.css('div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child(3)::text').get()
        kvadratura = response.css('div.property__amenities:nth-child(2) > ul:nth-child(2) > li:nth-child(3) > strong:nth-child(1)::text').get().strip() if 'Kvadratura' in kvadratura_tag else '-'

        yield { 
            'tip_nekretnine': 'Kuća',
            'tip_ponude': 'Izdavanje',
            'grad': response.css('.property__location > ul:nth-child(1) > li:nth-child(3)::text').get(),
            'deo_grada': response.css('.property__location > ul:nth-child(1) > li:nth-child(4)::text').get(),
            'kvadratura': kvadratura,
            'godina_izgradnje': godina_izgradnje,
            'povrsina_zemljista': response.css('.property__main-details > ul:nth-child(1) > li:nth-child(5) > span:nth-child(2)::text').get(),
            'broj soba': response.css('.property__main-details > ul:nth-child(1) > li:nth-child(2) > span:nth-child('
                                      '2)::text').get(),
            'tip_grejanja': response.css('.property__main-details > ul:nth-child(1) > li:nth-child(3) > '
                                         'span:nth-child(2)::text').get(),
            'parking': parking,
            'broj_kupatila': broj_kupatila
        }

    def parse(self, response):
        for link in response.css('div.row.offer div.offer-body h2.offer-title a::attr(href)').getall():
            nekretnina_details = response.urljoin(link)
            yield scrapy.Request(nekretnina_details, callback=self.dev)

        # Kada se dodje do poslednje nekretnine na stranici treba ici na drugu stranicu (dugme Sledeca strana) i ponoviti sve isto
        next_page = response.css('a.next-article-button::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print(f'Stranica ne postoji...Zavrsava se parsiranje')

# Dataset:

# xxx tip nekretnine (stan,kuca)
# xxx tip ponude (prodaja, izdavanje)
# xxx lokacija (grad + deo grada gde se nalazi)
# xxx kvadratura
# xxx godina izgradnje
# xxx povrsina zemljista (samo za kuce)
# xxx spratnost (ukupna i sprat na kom se nalazi; samo za stanove)
# uknjizenost (da/ne)
# xxx tip grejanja
# xxx ukupan broj soba
# xxx ukupan broj kupatila (toaleta)
# xxx podaci o parkingu (da/ne)

# ostalo:
# lift
# terasa i sl
#
#
