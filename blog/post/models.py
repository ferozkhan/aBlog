from django.db import models
from django.contrib import admin
from django.db.models import permalink
from django.utils.text import slugify
from django.utils.encoding import smart_text

import markdown
from django_markdown.models import MarkdownField


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    post = MarkdownField()
    post_html = models.TextField(null=True)
    posted = models.DateField(auto_now_add=True, db_index=True)
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.post = smart_text(self.post)
        self.post_html = markdown.markdown(self.post)
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        for tag in self.tags.all():
            tag.post_count += 1
            tag.save()

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, {'slug': self.slug})

    class Meta:
        ordering = ["-posted"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class PostAdmin(admin.ModelAdmin):
    exclude = ('slug', 'post_html')


class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    post_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.tag

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super(Tag, self).save(*args, **kwargs)


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'post_count')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
