from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category=models.ForeignKey(Category)
    title = models.CharField(max_length=200)
    summary=models.TextField()
    flesch_score = models.FloatField()
    sentiment_score = models.FloatField()
    subjectivity_score = models.FloatField()

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)

    def __unicode__(self):
        return self.user.username

