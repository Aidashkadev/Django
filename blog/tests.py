from django.test import TestCase
from django.urls import reverse
from .models import Blog


# ---------- Часть 1: тесты List и Detail ----------

class BlogListViewTests(TestCase):
    def setUp(self):
        self.blog1 = Blog.objects.create(title="Первый", content="Текст 1")
        self.blog2 = Blog.objects.create(title="Второй", content="Текст 2")

    def test_list_status_code(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_contains_content(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, "Первый")
        self.assertContains(response, "Второй")

    def test_list_empty(self):
        Blog.objects.all().delete()
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Первый")

    def test_list_has_links_with_id(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, reverse('blog_detail', args=[self.blog1.pk]))
        self.assertContains(response, reverse('blog_detail', args=[self.blog2.pk]))


class BlogDetailViewTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title="Статья", content="Содержимое")

    def test_detail_existing_id(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Содержимое")

    def test_detail_nonexistent_id(self):
        response = self.client.get(reverse('blog_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_link_from_list_opens_detail(self):
        url = reverse('blog_detail', args=[self.blog.pk])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].pk, self.blog.pk)

    def test_detail_template(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertTemplateUsed(response, 'blog/blog_detail.html')


# ---------- Часть 2: лайки ----------

class BlogLikesTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title="Тест", content="Текст статьи")

    def test_new_blog_has_zero_likes(self):
        self.assertEqual(self.blog.likes, 0)

    def test_detail_view_increments_likes(self):
        url = reverse('blog_detail', args=[self.blog.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.likes, 1)