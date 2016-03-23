# -*- coding: utf-8 -*-

from textstat.textstat import textstat
from textblob import TextBlob


def calculate_stats(content):

    try:
        testimonial = TextBlob(content)
        polarity = '%.3f'%(testimonial.sentiment.polarity)
        subjectivity = '%.3f'%(testimonial.sentiment.subjectivity)

        flesh_score = '%.3f'%(textstat.flesch_reading_ease(content))

        return {'polarity': polarity, 'subjectivity': subjectivity, 'flesh_score': flesh_score}
    except:
        return {'polarity': 0, 'subjectivity': 0, 'flesh_score': 0}


