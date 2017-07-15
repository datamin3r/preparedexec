# -*- coding: utf-8 -*-
#    
#    Based on vesion of Ben Goldsworthy Scrapping Alpha code   
#
#    Title: Scraping Alpha
#    Version: 1.0
#    Author: Ben Goldsworthy <b.goldsworthy@lancaster.ac.uk>
#
#    Amended:  12 April 2017
#    T Donoghue: tom.donoghue@gmail.com     
#    To cater for a new basic spider modified  to capture single earnings call.
#    Extracts only the Call info, 
#    Execs, analysts and the whole Q&A section trascript traversal. 
#    It now outputs the Individual asking the question and the exec
#    responding. Ommitting date, time and body line = None processing
#    Many thanks for the concepts and methods for extracting the opening actors.    

import scrapy

import codecs
import sys


# This enum lists the stages of each transcript.
from enum import Enum
Stage = Enum('Stage', 'preamble execs analysts body')
# Some transcript preambles are concatenated on a single line. This list is used
# To separate the title and date sections of the string.
#months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
transcripts = {}

sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

#TD modified as new sprider config created. 
class BasicSpider(scrapy.Spider):
    name = "basic"
    # TD Added Add a single url samples below
    '''
    start_urls = ['https://seekingalpha.com/article/4060920-constellation-'\
                  'brands-stz-ceo-robert-sands-q4-2017-results-earnings-call-transcript?part=single']
                  
    start_urls = ['https://seekingalpha.com/article/4051659-anheuser-'\
                  'buschs-bud-ceo-carlos-brito-q4-2016-results-earnings-call-transcript?part=single']
           
    start_urls = ['https://seekingalpha.com/article/4046011-molson-coors-'\
                  'brewings-tap-ceo-mark-hunter-q4-2016-results-earnings-call-transcript?part=single']
          
    start_urls = ['https://seekingalpha.com/article/4045632-treasury' \
                  '-wine-estates-tsryy-ceo-michael-clarke-2017-interim' \
                  '-results-earnings-call-transcript?part=single']

    start_urls = ['https://seekingalpha.com/article/4062418-wells-fargos-wfc' \
                  '-ceo-tim-sloan-q1-2017-results-earnings-call-transcript?part=single']
    '''
    #start_urls = ['https://seekingalpha.com/article/3994122-heinekens-heiny-ceo-jean-francois-van-'\
    #              'boxmeer-q2-2016-results-earnings-call-transcript?part=single']
        
    #start_urls = ['https://seekingalpha.com/article/4052880-brown-formans-bf-b-ceo-paul-varga-q3-2017-results-earnings-call-transcript?part=single']
    #start_urls = ['https://seekingalpha.com/article/4040247-unilevers-ul-ceo-paul-polman-q4-2016-results-earnings-call-transcript?part=single']
    #start_urls = ['https://seekingalpha.com/article/3388215-diageos-deo-ceo-ivan-menezes-on-q2-2015-results-earnings-call-transcript?part=single']
    #start_urls = ['https://seekingalpha.com/article/3235806-brown-formans-bf-b-ceo-paul-varga-on-q4-2015-results-earnings-call-transcript?part=single']
    #start_urls = ['https://seekingalpha.com/article/2870026-diageos-deo-ceo-ivan-menezes-on-q2-2015-results-earnings-call-transcript?part=single']
    
    #start_urls = ['https://seekingalpha.com/article/2362625-diageos-deo-ceo-ivan-menezes-on-q4-2014-results-earnings-call-transcript?part=single']
    #start_urls = ['https://seekingalpha.com/article/1715152-diageos-management-hosts-brunch-time-call-with-regional-president-transcript?part=single']

    #start_urls = ['https://seekingalpha.com/article/1587932-diageo-management-discusses-q4-2013-results-earnings-call-transcript??part=single']
    #start_urls = ['https://seekingalpha.com/article/1509242-molson-coors-brewing-companys-ceo-hosts-divisional-seminar-transcript??part=single']
    #start_urls = ['https://seekingalpha.com/article/1491422-diageo-plc-special-call?part=single']
    #start_urls = ['https://seekingalpha.com/article/1433871-diageos-management-hosts-brunch-time-call-with-the-presidents-conference-transcript?part=single']
    #start_urls = ['https://seekingalpha.com/article/1420911-diageo-plc-special-call?part=single']
    #start_urls = ['https://seekingalpha.com/article/1252141-diageos-management-hosts-brunch-time-call-with-the-presidents-conference-transcript?all=true&find=diageo?part=single']
    #start_urls = ['https://seekingalpha.com/article/4034667-constellation-brands-stz-ceo-robert-sands-q3-2017-results-earnings-call-transcript?part=single']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q3 2017 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q2 2017 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q1 2017 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q4 2016 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q3 2016 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q2 2016 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/Constellation Brands (STZ) CEO Robert Sands on Q1 2016 Results - Earnings Call Transcript _ Seeking Alpha.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/anheuser-busch-inbevs-bud-ceo-carlos-brito-q1-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/anheuser-busch-inbevs-bud-ceo-carlos-brito-q2-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/anheuser-busch-inbevs-bud-ceo-carlos-brito-q4-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/anheuser-busch-inbevs-bud-ceo-carlos-brito-q1-2017-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/diageos-management-hosts-brunch-time-call_05_14-with-regional-president-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/diageos-dgeaf-ceo-ivan-menezes-q4-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/diageos-deo-ceo-ivan-menezes-on-q2-2015-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/diageos-deo-ceo-ivan-menezes-on-q2-2015-1-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/diageos-deo-ceo-ivan-menezes-on-q4-2014-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/treasury-wine-estates-tsryy-ceo-michael-clarke-2017-interim-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/molson-coors-brewings-tap-ceo-mark-hunter-q1-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/molson-coors-brewings-tap-ceo-mark-hunter-q2-2016-results-earnings-call-transcript.htm']    
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/molson-coors-brewings-tap-ceo-mark-hunter-q3-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/molson-coors-brewings-tap-ceo-mark-hunter-q4-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/molson-coors-brewings-tap-ceo-mark-hunter-q1-2017-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/heineken-n-v-adr-heiny-ceo-jean-francois-van-boxmeer-on-q4-2014-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/heinekens-heiny-ceo-jean-francois-van-boxmeer-q2-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/heinekens-heiny-ceo-jean-francois-van-boxmeer-q4-2016-results-earnings-call-transcript.htm']
    #start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/brown-formans-bf-b-ceo-paul-varga-q3-2017-results-earnings-call-transcript.htm']
    start_urls = ['file:///C:/Users/tomd/Documents/MSCDA/ADM/pernod-ricards-pdrdf-ceo-pierre-pringuet-on-q4-2014-results-earnings-call-transcript.html']
    #TD Functions removed and this renamed
    def parse(self, response):
        i = 0
        transcript = {}
        details = {}
        execs = []
        analysts = []
        #script = []
        # TD 
        qa = []
        #qe = []
        mode = 1
        
        # TD - Modified to take all p elements in the a-body div
        body = response.css('div#a-body p')
        #body = response.xpath('//div[@id="a-body"]//p[@class="p p1"]')
        # TD Modified to select p elements  
        chunks = body.css('p')
        #print len(chunks) 
        while i < len(chunks):   
            # If the current line is a heading and we're not currently going
            # through the transcript body (where headings represent speakers),
            # change the current section flag to the next section.
            if (len(chunks[i].css('strong::text').extract()) == 0) or (mode == 4):
                #print i
                currStage = Stage(mode)
                #print currStage # If we're on the preamble stage, each bit of data is extracted
                # separately as they all have their own key in the JSON.
                if currStage == Stage['preamble']:
                    # If we're on the first line of the preamble, that's the
                    # company name, stock exchange and ticker acroynm (or should
                    # be - see below)
                    if i == 0:
                        #print str(i) + 'in preamble'
                        # Checks to see if the second line is a heading. If not,
                        # everything is fine.
                        if len(chunks[1].css('strong::text').extract()) == 0:
                            #tink = chunks[1].css('strong::text').extract()
                            #print tink + ' in preamble'
                            details['company'] = chunks[i].css('p::text').extract_first()
                            #print details['company']
                            if " (" in details['company']:
                                details['company'] = details['company'].split(' (')[0]
                            # If a specific stock exchange is not listed, it
                            # defaults to NYSE
                            details['exchange'] = "NYSE"
                            details['ticker'] = chunks.css('a::text').extract_first()
                            if ":" in details['ticker']:
                                ticker = details['ticker'].split(':')
                                details['exchange'] = ticker[0]
                                details['ticker'] = ticker[1]
                        # However, if it is, that means this line contains the
                        # full, concatenated preamble, so everything must be 
                        # extracted here
                        else:
                            details['company'] = chunks[i].css('p::text').extract_first()
                            #tinkComp = chunks[i].css('p::text').extract_first()
                            #print tinkComp + ' in preamble'
                            #print details['company']
                            if " (" in details['company']:
                                details['company'] = details['company'].split(' (')[0]
                            # if a specific stock exchange is not listed, default to NYSE
                            details['exchange'] = "NYSE"
                            details['ticker'] = chunks.css('a::text').extract_first()
                            if ":" in details['ticker']:
                                ticker = details['ticker'].split(':')
                                details['exchange'] = ticker[0]
                                details['ticker'] = ticker[1]
                                #print details['ticker']
                            '''TD Modified - not required
                       titleAndDate = chunks[i].css('p::text').extract[1]
                            for date in months:
                                if date in titleAndDate:
                                    splits = titleAndDate.split(date)
                                    details['title'] = splits[0]
                                    details['date'] = date + splits[1]
                      ''' 
                    # Otherwise, we're onto the title line.
                    elif i == 1:
                        title = chunks[i].css('p::text').extract_first()
                        # This should never be the case, but just to be careful
                        # I'm leaving it in.
                        if len(title) <= 0:
                            title = "NO TITLE"
                        details['title'] = title
                    # TD modified - not required
                    # Or the date line.
                    #elif i == 2:
                    #    details['date'] = chunks[i].css('p::text').extract_first()
                # If we're onto the 'Executives' section, we create a list of
                # all of their names, positions and company name (from the 
                # preamble).
                elif currStage == Stage['execs']:                    
                    anExec = chunks[i].css('p::text').extract_first().split(" - ")
                    #print ' execs here ' + str(chunks[i].css('p::text').extract_first().split(" - "))
                    # This covers if the execs are separated with an em- rather
                    # than an en-dash (see above).
                    if len(anExec) <= 1:
                        anExec = chunks[i].css('p::text').extract_first().split(" – ").decode('utf-8')
                    name = anExec[0]
                    #print ' exec name' + name
                    if len(anExec) > 1:
                        position = anExec[1]
                        #print ' exec pos ' + position
                    # Again, this should never be the case, as an Exec-less
                    # company would find it hard to get much done.
                    else:
                        position = ""
                    execs.append((name,position,details['company']))
                    #print str(execs)
                # This does the same, but with the analysts (which never seem
                # to be separated by em-dashes for some reason).
                elif currStage == Stage['analysts']:
                    name = chunks[i].css('p::text').extract_first().split(" - ")[0]
                    company = chunks[i].css('p::text').extract_first().split(" - ")[1]
                    analysts.append((name,company))
                    #print str(analysts)
                # This strips the transcript body of everything except simple
                # HTML, and stores that.
                elif currStage == Stage['body']:
                    line = chunks[i].css('p::text').extract_first()
                    #TD modified - not required html tags
                    #html = "p>"
                    if line is None:    
                        line = chunks[i].css('strong::text').extract_first()
                        #html = "h1>"
                    #TD modified do not want the whole body transcript text
                    #script.append("<"+html+line+"</"+html)
                    #else:
                        #self.log(" speaker: %s" % chunks[i].css('strong::text').extract_first())
                        #script.append("<"+html+line+"</"+html)
                        #script.append("["+line+"],")

            else:
                
                mode += 1
            i += 1
        
        #TD Addded - to get all Q&A transcript in one go 
        qust1= response.xpath('//p[@id="question-answer-session"]/following-sibling::p[preceding::div]/text()'+" | "+ '\
                              //p[@id="question-answer-session"]/following-sibling::p[preceding::div]//span/text()').extract()
        # TD Added - to loop through and get each Q&A  
        for aq in qust1:
            qa.append(aq)
            
       # Adds the various arrays to the dictionary for the transcript
        details['exec'] = execs 
        details['analysts'] = analysts
        #details['transcript'] = ''.join(script)
        #TD Added - To output Q&A section
        details['questions'] = qa
        # Adds this transcript to the dictionary of all scraped
        # transcripts, and yield that for the output
        transcript["entry"] = details
        #TD Modifies to return results
        return transcript