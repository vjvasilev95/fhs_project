import html_parser
from models import Category, Page

def calculate_stats(source, soup):
    if 'source' == 'healthgov':


        content = soup.select(".entry-content-top")
        content.append(soup.select(".entry-content-main"))
        content.append(soup.select(".page"))
        content_string = ""

        for div in content:
            content_string += str(div)

        content_string = html_parser.strip_tags(content_string)
        content_string = unicode(content_string, "utf-8")

        testimonial = TextBlob(content_string)

        polarity = testimonial.sentiment.polarity
        subjectivity = testimonial.sentiment.subjectivity

        flesh_score = textstat.flesch_reading_ease(content_string)

        page = Page(category = category, title = title, summary = summary, url = url, flesch_score = flesh_score, sentiment_score = polarity, subjectivity_score = subjectivity)
        page.save()

    elif source == 'bing':
        soup = html_parser.strip_tags(soup)
        soup = unicode(soup, "utf-8")
        page = Page(category = category, title = title, summary = summary, url = url)
        page.save()

    else:
        page = Page(category = category, title = title, summary = summary, url = url)
        page.save()