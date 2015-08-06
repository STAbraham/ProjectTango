from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

#This is called the urlpatterns "definition"; like you're defining any variable, in the form of a tuple
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls', namespace = 'rango')), #Adds app specific urls.py file
    (r'^accounts/', include('registration.backends.simple.urls', namespace = 'reg_redux')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
        )
