import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fhs_project.settings')

import django
django.setup()

from fhs.models import Category, Page
from django.contrib.auth.models import User
import random
from fhs.save_page_helper import *

def populate():
    python_cat = add_cat('General Information')

    add_page(cat=python_cat,
        title="Laboratory Tests ",
        url="https://www.nlm.nih.gov/medlineplus/laboratorytests.html",
        source="medline",
        summary="No description provided")

    add_page(cat=python_cat,
        title="Get Tested for Breast Cancer",
        url="http://healthfinder.gov/HealthTopics/Category/doctor-visits/screening-tests/get-tested-for-breast-cancer",
        source="healthgov",
        summary="No description provided")

    add_page(cat=python_cat,
        title="Association of UK Hospitals",
        url="http://www.aukuh.org.uk/",
        source="bing",
        summary="No description provided")

    django_cat = add_cat("Mothers' stuff")

    add_page(cat=django_cat,
        title="Get a Bone Density Test ",
        url="http://healthfinder.gov/HealthTopics/Category/doctor-visits/screening-tests/get-a-bone-density-test",
        source="healthgov",
        summary="No description provided")

    add_page(cat=django_cat,
        title="Top 20 sites for pregnant mothers",
        url="http://www.babble.com/pregnancy/20-web-sites-pregnant-women-should-know-and-love/",
        source="bing",
        summary="No description provided")

    add_page(cat=django_cat,
        title="Modern Moms",
        url="http://www.modernmom.com/",
        source="bing",
        summary="No description provided")

    frame_cat = add_cat("Light conditions")

    add_page(cat=frame_cat,
        title="Health Screening ",
        url="https://www.nlm.nih.gov/medlineplus/healthscreening.html",
        source="medline",
        summary="No description provided")

    add_page(cat=frame_cat,
        title="The flu: what to do when you get sick",
        url="http://www.cdc.gov/flu/takingcare.htm",
        source="bing",
        summary="No description provided")


def add_page(cat, title, url, source, summary):
    try:
        content = filter_content(source, url)
    except ValueError as e:
        content = ""
    stats = calculate_stats(content)
    p = Page.objects.get_or_create(category = cat, title = title, summary = summary, url = url, source = source,
                    flesch_score = stats['flesh_score'], sentiment_score = stats['polarity'], subjectivity_score = stats['subjectivity'])[0]
    #p = Page.objects.get_or_create(category=cat, title=title)[0]
    #p.url=url

    p.save()
    return p

def add_cat(name):
    #picking a random user for the category
    users = User.objects.all()
    lengthOfList = len(users)
    c = Category.objects.get_or_create(shared = True, name=name, user = users[random.randint(0, lengthOfList - 1)])[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting FHS cat_page population script..."
    populate()