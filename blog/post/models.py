from django.db import models
from django.contrib import admin
from django.db.models import permalink

from django_markdown.models import MarkdownField


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    post = MarkdownField()
    posted = models.DateField(auto_now_add=True, db_index=True)
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tags')

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, {'slug': self.slug})


class Tags(models.Model):
    tag = models.CharField(max_length=20)

    def __unicode__(self):
        return self.tag


admin.site.register(Post)
admin.site.register(Tags)
