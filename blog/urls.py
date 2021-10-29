from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
  path('articles/', views.ArticleListView.as_view(), name='articles'),
  path('recent_news/', views.recent_news, name='recent_views'),
  path('categories/<str:slug>/', views.CategoryArticleView.as_view(), name='category'),
  path('articles/<str:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
  path('num_views_object/<str:slug>/', views.num_views_object, name='num_views_object'),
]
