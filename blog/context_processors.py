from .models import Category

def category_list(request):
  categories = Category.objects.filter(status=Category.ACTIVE)

  if request.method == 'GET':
    return {
      'categories': categories
    }
