from django.db.models import F
from django.views.generic import ListView, DetailView
from .models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Blog.objects.filter(pk=obj.pk).update(likes=F('likes') + 1)
        obj.refresh_from_db()
        return obj