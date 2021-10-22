from django.urls import path
from .views import CategoryArticleView

app_name = 'blog'

urlpatterns = [
  path('<str:slug>/', CategoryArticleView.as_view(), name='category')
]
