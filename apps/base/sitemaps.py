from django.contrib.sitemaps import Sitemap
from apps.articles.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return "/articles/%s" % (obj.slug)
