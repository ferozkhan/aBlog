
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from post.models import Post, Tag
from django.utils import timezone


class PostList(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'blog_posts'
    # paginate_by = 5

    def get_context_data(self, **kwargs):
        self.context = super(PostList, self).get_context_data(**kwargs)
        self.context['tags'] = Tag.objects.all()
        return self.context


class PostView(DetailView):
    template_name = 'post/post_view.html'
    context_object_name = 'blog_post'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['now'] = timezone.now()
        return context


class TagView(SingleObjectMixin, ListView):
    model = Post
    context_object_name = 'blog_posts'
    template_name = 'post/post_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        return super(TagView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['blog_posts'] = self.object.post_set.all()
        return context
