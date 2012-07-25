from django.conf.urls import patterns, include, url

urlpatterns = patterns('coffeeweb.views',
    (r'^$', 'index'),
)