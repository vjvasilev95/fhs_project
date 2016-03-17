from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    description = models.CharField(max_length=500,null=True)
    shared = models.BooleanField(default=False)
    slug = models.SlugField()
    #
    def save(self, *args, **kwargs):
    #     # Uncomment if you don't want the slug to change every time the name changes
    #     #if self.id is None:
    #     #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    category=models.ForeignKey(Category)
    title = models.CharField(max_length=200)
    summary=models.TextField(default="test")
    flesch_score = models.FloatField(default=0)
    sentiment_score = models.FloatField(default=0)
    subjectivity_score = models.FloatField(default=0)
    url = models.URLField(default="http://medlineplus.com")

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

