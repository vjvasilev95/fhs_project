import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fhs_project.settings')

import django
django.setup()

from fhs.models import Category, Page
from django.contrib.auth.models import User
import random

def populate():
    python_cat = add_cat('General Information')

    add_page(cat=python_cat,
        title="NHS",
        url="http://www.nhs.uk/pages/home.aspx")

    add_page(cat=python_cat,
        title="South Glasgow Hospital",
        url="http://www.nhsggc.org.uk/patients-and-visitors/main-hospital-sites/queen-elizabeth-university-hospital-campus/")

    add_page(cat=python_cat,
        title="Association of UK Hospitals",
        url="http://www.aukuh.org.uk/")

    django_cat = add_cat("Mothers' stuff")

    add_page(cat=django_cat,
        title="Kelly Mom: Breastfeeding and parenting",
        url="http://kellymom.com/")

    add_page(cat=django_cat,
        title="Top 20 sites for pregnant mothers",
        url="http://www.babble.com/pregnancy/20-web-sites-pregnant-women-should-know-and-love/")

    add_page(cat=django_cat,
        title="Modern Moms",
        url="http://www.modernmom.com/")

    frame_cat = add_cat("Light conditions")

    add_page(cat=frame_cat,
        title="10 reminders when you have a flu",
        url="http://www.webmd.com/cold-and-flu/features/treating-flu-at-home")

    add_page(cat=frame_cat,
        title="The flu: what to do when you get sick",
        url="http://www.cdc.gov/flu/takingcare.htm")


def add_page(cat, title, url):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.save()
    return p

def add_cat(name):
    #picking a random user for the category
    users = User.objects.all()
    lengthOfList = len(users)
    c = Category.objects.get_or_create(name=name, user = users[random.randint(0, lengthOfList - 1)])[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting FHS cat_page population script..."
    populate()