from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator

from .models import Article, Category

class HomeView(generic.ListView):
  model = Article
  template_name = 'blog/home/index.html'
  context_object_name = 'article_list'

class CategoryArticleView(generic.DetailView):
  model = Category
  template_name = 'blog/category.html'

  def get_queryset(self):
    return super().get_queryset().filter(status=Category.ACTIVE)

  def get_context_data(self, **kwargs):
    category = self.object
    articles = category.article_set.filter(status=Article.PUBLISHED)
    per_page = 10

    paginator = Paginator(articles, per_page)
    page_number = self.request.GET.get('page')

    context = super().get_context_data(**kwargs)
    context['page_articles'] = paginator.get_page(page_number)

    return context
