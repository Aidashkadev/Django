from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemModelTests(TestCase):
    def test_str_returns_title(self):
        """__str__ возвращает название записи."""
        item = Item.objects.create(title="Тест")
        self.assertEqual(str(item), "Тест")

    def test_absolute_url(self):
        """get_absolute_url ведёт на страницу детали."""
        item = Item.objects.create(title="Тест")
        self.assertEqual(item.get_absolute_url(), reverse("crud:detail", args=[item.pk]))


class ItemListViewTests(TestCase):
    def test_list_empty(self):
        """Пустой список показывает заглушку."""
        response = self.client.get(reverse("crud:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пока ничего нет")

    def test_list_shows_items(self):
        """Список показывает созданные записи."""
        Item.objects.create(title="Первая")
        Item.objects.create(title="Вторая")
        response = self.client.get(reverse("crud:list"))
        self.assertContains(response, "Первая")
        self.assertContains(response, "Вторая")
        self.assertEqual(len(response.context["items"]), 2)


class ItemDetailViewTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(title="Деталь", description="Описание")

    def test_detail_ok(self):
        """Страница детали возвращает содержимое записи."""
        response = self.client.get(reverse("crud:detail", args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Деталь")
        self.assertContains(response, "Описание")

    def test_detail_404_for_missing_id(self):
        """Несуществующий id даёт 404."""
        response = self.client.get(reverse("crud:detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_list_link_navigates_to_detail(self):
        """Ссылка из списка реально ведёт на страницу детали."""
        response = self.client.get(reverse("crud:list"))
        self.assertContains(response, reverse("crud:detail", args=[self.item.pk]))


class ItemCreateTests(TestCase):
    def test_create_get_form(self):
        """GET на создание отдаёт форму."""
        response = self.client.get(reverse("crud:create"))
        self.assertEqual(response.status_code, 200)

    def test_create_post_valid(self):
        """Валидный POST создаёт запись и делает редирект."""
        response = self.client.post(reverse("crud:create"), {"title": "Новая", "description": "x"})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_create_post_invalid(self):
        """POST без названия не создаёт запись."""
        response = self.client.post(reverse("crud:create"), {"title": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)


class ItemUpdateTests(TestCase):
    def test_update_changes_title(self):
        """POST на изменение обновляет запись."""
        item = Item.objects.create(title="Старое")
        self.client.post(reverse("crud:update", args=[item.pk]), {"title": "Новое", "description": ""})
        item.refresh_from_db()
        self.assertEqual(item.title, "Новое")


class ItemDeleteTests(TestCase):
    def test_delete_removes_item(self):
        """POST на удаление убирает запись."""
        item = Item.objects.create(title="Удалить")
        response = self.client.post(reverse("crud:delete", args=[item.pk]))
        self.assertEqual(Item.objects.count(), 0)
        self.assertRedirects(response, reverse("crud:list"))
