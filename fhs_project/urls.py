from django.conf.urls import patterns, include, url
from django.contrib import admin
import django.contrib.auth


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fhs_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^fhs/', include('fhs.urls')),

)
