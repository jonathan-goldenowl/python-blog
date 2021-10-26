from django.urls import path
from .views import CategoryArticleView, ArticleDetailView, num_views_object

app_name = 'blog'

urlpatterns = [
  path('<str:slug>/', CategoryArticleView.as_view(), name='category'),
  path('article/<str:slug>/', ArticleDetailView.as_view(), name='article_detail'),
  path('num_views_object/<str:slug>/', num_views_object, name='num_views_object'),
]
