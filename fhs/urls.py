from django.conf.urls import patterns, include, url
import views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
        url(r'^$', views.index, name="index"),
        url(r'^register/$', views.register, name="register"),
        url(r'^login/$', views.user_login, name="login"),
        url(r'^logout/$', views.user_logout, name="logout"),
        url(r'^about/$', views.about, name="about"),
        url(r'^privacy-policy/$', views.privacy, name="privacy"),
        url(r'^terms-of-use/$', views.terms, name="terms"),
        url(r'^search/', views.search, name='search'),
        url(r'^save-page/', views.save_page, name='save_page'),
        url(r'^add_category/', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^profile/(?P<user>[-\w.]+)/$', views.profile, name='profile'),
        url(r'^editprofile/', views.editprofile, name='editprofile'),
        url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
        url(r'^password-change/$', auth_views.password_change, {'template_name': 'fhs/changepassword.html'},name='userauth_password_change'),
        url(r'^password-change-done/$', auth_views.password_change_done, {'template_name': 'fhs/changepassworddone.html'}, name='password_change_done'),
        url(r'^goto/$', views.track_category, name='goto'),
        )