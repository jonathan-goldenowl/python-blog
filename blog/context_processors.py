from .models import Article, Category

def category_list(request):
  if request.method == 'GET':
    categories = Category.objects.filter(status=Category.ACTIVE)
    popular_posts = Article.objects.filter(status=Article.PUBLISHED).order_by('-num_views', '-created_at')[:4]

    return {
      'categories': categories,
      'popular_posts': popular_posts,
    }

  return {}
