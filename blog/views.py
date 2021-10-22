from django.http import JsonResponse
from django.views import generic
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

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
