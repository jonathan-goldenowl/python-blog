from django.contrib import admin

from .models import Author, Article ,Category

admin.site.register(Author)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_per_page = 20
  search_fields = ['title']

  list_display = ('title', 'description', 'cover_image_tag', 'status', 'created_at', 'updated_at')
  list_filter = ('featured', 'status', 'category', 'created_at')

  exclude = ('uuid', 'num_views')
  fieldsets = (
    (None, {
      'fields': ('title', 'description', 'cover_image', 'status', 'category', 'author', 'featured'),
    }),
    ('Advanced options', {
      'classes': ('collapse',),
      'fields': ('slug',),
    }),
  )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  search_fields = ['title']
  list_display = ('title', 'description', 'featured')
