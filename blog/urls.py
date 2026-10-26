from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('items/', include('crud.urls')),
]