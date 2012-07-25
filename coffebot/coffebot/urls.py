from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# from coffebot.coffeeweb import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coffebot.views.home', name='home'),
    # url(r'^coffebot/', include('coffebot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^coffee/', include('coffeeweb.urls')),
)
