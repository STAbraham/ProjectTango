from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^search/$', views.search, name='search'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^add_profile/$', views.register_profile, name='profile')
    ,)

"""
The following is the non-querystring way to implement the url to track_url. Corresponding changes will have
to be made to the actual track_url view and "category.html". Refactoring to use querystrings so that you have an understanding
of how to implement.
"""
    # url(r'^goto/(?P<page_id>[\w\-}]+)/$', views.track_url, name='goto')

"""
Below URLs were used when we build a custom register, login, and logout
flow. Helpful for educational/informational purposes
"""
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout')