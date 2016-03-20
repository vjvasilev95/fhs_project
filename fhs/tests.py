from django.test import TestCase

from fhs.models import Category
from django.contrib.auth.models import User


class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        newuser = User(username="me")
        newuser.save()
        cat = Category(name='test',views=-1)
        cat.user=newuser
        cat.save()
        self.assertEqual((cat.views >= 0), True)



