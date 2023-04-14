from django.contrib import admin

from .models import Article, ArticleMeta, Category

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ArticleMeta)
