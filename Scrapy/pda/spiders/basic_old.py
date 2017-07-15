# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.loader import ItemLoader
from pda.items import PdaItem
#from enum import Enum

#Stage = Enum('Stage', 'preamble execs analysts body')
class tparts:
    head, execty, analty, bods = range(4)


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["web"]
    start_urls = ['https://seekingalpha.com/article/4045632-treasury' \
                  '-wine-estates-tsryy-ceo-michael-clarke-2017-interim' \
                  '-results-earnings-call-transcript']
    #?part=single']
    #start_urls = ['http://example.com']



    def parse(self, response):
        p1ItemCount = 0
        stp = 0
        trans = {}
        mode = 1
        currStage = tparts.head
        print tparts.head
        parts = {}
        execs = []
        anlyst = []
        qa = []
        #transcript = []
        #parts = {}
        #p1ItemCount = 3
        page1 = response.xpath('//div[@id="a-body"]//p[@class="p p1"]')
        print 'start whe'
        while stp < 10:
            #currStage = Stage(mode)
            #print currStage 
            if currStage == tparts.head:
                print tparts.head 
                if p1ItemCount == 0:
                    org = page1[p1ItemCount].css('.p1::text').extract()
                    #trimOrg =  org.strip(" (") #str(org.replace(" (", ""))
                    parts['org'] = org 
                    print parts
                    #currStage = tparts.execty
                    print str(currStage) + ' currStage end head'
                    p1ItemCount += 1 #testing
            elif currStage == tparts.execty: 
                #if p1ItemCount > 0 and p1ItemCount < len(page1):
                print str(p1ItemCount) + ' in execc'
                # need to loop thru the execs and spit ou ttheir names
                if len(page1[p1ItemCount].css('strong::text').extract()) == 0:
                    actorName = page1[p1ItemCount].css('.p1::text').extract()
                    print actorName
                    execs.append(actorName)
                    print 'execs' + str(p1ItemCount)
                else:
                    heading = page1[p1ItemCount].css('strong::text').extract()
                    print 'heading ' + str(heading)
            elif currStage == tparts.analty:
                anExec = page1[p1ItemCount].css('p::text').extract_first()
                print 'anal'
                print anExec
            elif currStage == tparts.bods:
                print 'body'
            print 'stp incr ' + str(stp)
            stp +=1
            print 'stp after inc ' + str(stp)
            print p1ItemCount
            p1ItemCount += 1  
            currStage += 1
            print '---'
            print currStage
            #mode += 1
            #print mode
 
        '''
        for node in response.xpath('//*[@id="a-body"]//p'):
            transcript.append(node.css('::text').extract())
        trans['out'] = transcript
        '''
        #self.log("transout: %s" % response.xpath('//*[@id="a-body"]/p[3]/text()').extract())
        #--l = ItemLoader(item = PdaItem(), response=response)
        #l.add_xpath('transout', '//*[@id="a-body"]//p')
        #--l.add_xpath('transout', '//*[@id="a-body"]/p[3]/text()')
        #item = PdaItem()
        #item['transout'] = response.xpath('//*[@id="a-body"]/p[3]/text()').extract()
        #transcript = response.xpath('//*[@id="a-body"]/p[3]/text()').extract()
        '''
        filename = 'inittrnscrpt.txt' 
        with open(filename, 'wb') as f:
            f.write(str(trans))
        self.log('Saved file ')
        '''
        #--return l.load_item()
        #return
        #pass
