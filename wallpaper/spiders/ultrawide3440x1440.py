# -*- coding: utf-8 -*-
import scrapy
import logging
import urlparse
from scrapy.shell import inspect_response
from wallpaper.items import WallpaperItem


class Ultrawide3440x1440Spider(scrapy.Spider):
    name = 'ultrawide3440x1440'
    allowed_domains = ['wallpaperswide.com']
    prefixurl= 'http://wallpaperswide.com'

    def start_requests(self):
        urls = [
            'http://wallpaperswide.com/lakes-desktop-wallpapers/page/',
            'http://wallpaperswide.com/landscape-desktop-wallpapers/page/',
            'http://wallpaperswide.com/beach-desktop-wallpapers/page/',
            'http://wallpaperswide.com/desert-desktop-wallpapers/page/',
            'http://wallpaperswide.com/forests-desktop-wallpapers/page/',
            'http://wallpaperswide.com/mountains-desktop-wallpapers/page/',
            'http://wallpaperswide.com/rivers-desktop-wallpapers/page/',
            'http://wallpaperswide.com/sun__sky-desktop-wallpapers/page/',
            'http://wallpaperswide.com/waterfalls-desktop-wallpapers/page/'
        ]

        for url in urls:
            for i in range(1, 3):
                #pageurl = urlparse.urljoin(urls[0], i)
                pagedd = "{}{}/".format(url, i)
                #self.logger.info("start_requests %s", pagedd)
                yield scrapy.Request(url=pagedd, callback=self.parse)

    def parse(self, response):
        self.logger.info("parse %s", response.url)
        pagelinks = response.xpath('//li[@class="wall"]/div/a/@href').extract()
        for pageurl in pagelinks:
            realurl = urlparse.urljoin(self.prefixurl, pageurl)
            #self.logger.info("%s", realurl)
            request = scrapy.Request(realurl, callback=self.parse_Img)
            yield request

    def parse_Img(self, response):
        #self.logger.warning("parse ImgPage %s", response.url)
        #inspect_response(response, self)
        imgurl = response.xpath('//a/@href').re_first(r'[\d|\D]*-3440x1440\.jpg$')

        if imgurl:
            realurl = urlparse.urljoin(self.prefixurl, imgurl)
            self.logger.warning("parseImgurl %s", realurl)
            item = WallpaperItem()
            item['file_urls'] = [realurl]
            return item

        #self.logger.warning("parseImg %s", response.xpath('//a/@href').re_first(r'[\d|\D]*-3440x1440\.jpg$'))
