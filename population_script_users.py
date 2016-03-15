import string
import random

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fhs_project.settings')

import django
django.setup()

from fhs.models import UserProfile
from django.contrib.auth.models import User

def populate_users():
    f1 = open("users.txt", "r")

    line = f1.readline()[: -1]

    while len(line) != 0:
        list = string.split(line, " ")
        family_name = list[0]
        given_name = list[1]
        initial = list[2]
        gender = list[3]
        email = "{}.{}@fmail.com".format(given_name, family_name)
        #create a "random" purely numeric password
        password = ""
        for i in range(20):
            password += str(random.randint(0, 9))
        #create the user object
        theUser = User()
        theUser.username = "{}.{}".format(given_name, family_name)
        theUser.first_name = given_name
        theUser.last_name = family_name
        theUser.email = email
        theUser.password = password
        #hash the password
        theUser.set_password(theUser.password)

        #save the user to the db
        theUser.save()

        #create the userProfile object
        profile = UserProfile()
        profile.user = theUser
        profile.save()
        line = f1.readline()[: -1]


if __name__ == '__main__':
    print "Starting FHS user population script..."
    populate_users()








