from typing import Any, Dict
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.db.models import OuterRef, Subquery, Prefetch

from .models import Article, Category

class HomeView(generic.ListView):
  model = Article
  template_name = 'blog/home/index.html'
  context_object_name = 'article_list'

  def get_context_data(self, **kwargs) -> Dict[str, Any]:
    featured_article = Article.objects.filter(status=Article.PUBLISHED, featured=True).order_by('?').first()

    # Subquery
    subqry = Subquery(Article.objects
      .filter(category_id=OuterRef('category_id'), status=Article.PUBLISHED)
      .values_list('id', flat=True)[:3])

    # Prefetch article set to prevent N+1 issue
    featured_categories = Category.objects.filter(featured=True).order_by('title')\
      .prefetch_related(
        Prefetch('article_set', queryset=Article.objects.filter(id__in=subqry))
      )

    context = super(HomeView, self).get_context_data(**kwargs)
    context['featured_categories'] = featured_categories
    context['featured_article'] = featured_article
    return context

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

    context = super(CategoryArticleView, self).get_context_data(**kwargs)
    context['page_articles'] = paginator.get_page(page_number)

    return context

class ArticleDetailView(generic.DetailView):
  model = Article
  template_name = 'blog/article_detail.html'

def num_views_object(request, slug):
  if request.method == 'POST':
    try:
      article = Article.objects.filter(status=Article.PUBLISHED).get(slug=slug)
      article.num_views += 1
      article.save()

      dict_article = model_to_dict(article, exclude=['cover_image'])
      dict_article['cover_image_url'] = article.cover_image.url

      return JsonResponse({ 'success': True, 'article': dict_article })
    except Article.DoesNotExist as ex:
      return JsonResponse({ 'success': False, 'message': ex }, status=404)
    except Exception as ex:
      return JsonResponse({ 'success': False, 'message': ex }, status=500)

def recent_news(request):
  html = ""
  articles = Article.objects.filter(status=Article.PUBLISHED).order_by('-updated_at', '-created_at')[:6]
  paginator = Paginator(articles, 3)
  page_number = request.GET.get('page')
  recent_news = paginator.get_page(page_number)

  for article in recent_news:
    html += render_to_string('blog/partials/article_item.html', { 'article': article })

  html += render_to_string('blog/home/pagy_recent_news.html', { 'recent_news': recent_news })

  return HttpResponse(html)
