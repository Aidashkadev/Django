from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import ItemForm
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = "crud/item_list.html"
    context_object_name = "items"


class ItemDetailView(DetailView):
    model = Item
    template_name = "crud/item_detail.html"
    context_object_name = "item"


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = "crud/item_form.html"


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "crud/item_form.html"


class ItemDeleteView(DeleteView):
    model = Item
    template_name = "crud/item_confirm_delete.html"
    success_url = reverse_lazy("crud:list")
