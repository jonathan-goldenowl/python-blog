from django.contrib import admin

from .models import Author, Article ,Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'cover_image_tag', 'status', 'category', 'author', 'created_at', 'updated_at')
  exclude = ('uuid', 'num_views')
  fieldsets = (
    (None, {
      'fields': ('title', 'description', 'cover_image', 'status', 'category', 'author'),
    }),
    ('Advanced options', {
      'classes': ('collapse',),
      'fields': ('slug',),
    }),
  )

admin.site.register(Author)
admin.site.register(Category)
