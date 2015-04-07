from django.conf.urls import patterns, include, url
from django.contrib import admin
from post.views import PostList, PostView, TagView

from django.views import generic


urlpatterns = patterns('',
    url(r'^$', PostList.as_view()),
    url(r'^post/(?P<slug>[^\.]+).html', PostView.as_view()),
    url(r'^tag/(?P<slug>[^\.]+).html', TagView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    url('^markdown/', include( 'django_markdown.urls')),
)
