# -*- coding: utf-8 -*-

from textstat.textstat import textstat
from textblob import TextBlob
from bs4 import BeautifulSoup
import urllib
import urllib2
import html_parser

def calculate_stats(content):

    try:
        testimonial = TextBlob(content)
        polarity = '%.3f'%(testimonial.sentiment.polarity)
        subjectivity = '%.3f'%(testimonial.sentiment.subjectivity)

        flesh_score = '%.3f'%(textstat.flesch_reading_ease(content))

        return {'polarity': polarity, 'subjectivity': subjectivity, 'flesh_score': flesh_score}
    except:
        return {'polarity': 0, 'subjectivity': 0, 'flesh_score': 0}


def filter_content(source, url):

    try:
        html_file = urllib2.urlopen(url)
        html_doc = html_file.read()
        html_file.close()
        soup = BeautifulSoup(html_doc, 'html.parser')
    except:
        raise ValueError("Unable to load the page")

    if source == 'healthgov':
        content = soup.select(".entry-content-top")
        content.append(soup.select(".entry-content-main"))
        content.append(soup.select(".page"))
        content_string = ""

        for div in content:
            content_string += str(div)

        content_string = html_parser.strip_tags(content_string)
        content_string = unicode(content_string, "utf-8")

        return content_string

    elif source == 'medline':

        content = str(soup.select("#topic-summary"))
        content_string = html_parser.strip_tags(content)
        content_string = unicode(content_string, "utf-8")
        return content_string

    else:

        soup = str(soup.body)

        try:
            content_string = html_parser.strip_tags(soup)

            content_string = unicode(content_string, "utf-8")

            return content_string
        except:
            return soup

