import string
import random

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fhs_project.settings')

import django
django.setup()

from fhs.models import UserProfile
from django.contrib.auth.models import User


# Add the three special users

def populate_users_special():
    f1 = open("users.txt")
    line = f1.readline()[: -1]
    while len(line) != 0:
        theUser = User()
        theUser.username = line
        theUser.first_name = line
        theUser.email = "{}@gmail.com".format(line)
        theUser.password = line
        theUser.set_password(theUser.password)
        theUser.save()
        profile = UserProfile()
        profile.user = theUser
        profile.save()
        line = f1.readline()[: -1]


if __name__ == '__main__':
    print "Starting FHS user population script..."
    populate_users_special()








