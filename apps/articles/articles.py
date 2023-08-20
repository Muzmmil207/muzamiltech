import requests

from django.conf import settings
from django.template.defaultfilters import slugify
from utils.data_collector import DataCollector

from .models import Article, Category


class ArticleCollector(DataCollector):
    model = Article
    URLs = {"newsdata": f"https://newsdata.io/api/1/news?apikey={settings.NEWSDATA_API_KEY}"}

    def newsdata(self, query):
        count = 0
        url = self.URLs.get("newsdata")
        to_date, from_date = self.get_time(from_date=1)
        payload = {
            "q": query,
            "from_date": from_date,
            "to_date": to_date,
            "category": "technology",
            "language": "en",
        }
        response = requests.get(url, params=payload)
        data = response.json()
        articles = data["results"]
        for article in articles:
            try:
                article_obj = self.model(
                    title=article.get("title", ""),
                    meta_title=article.get("title", ""),
                    slug=slugify(article.get("title", "")),
                    description=article.get("description", "").replace("/PRNewswire/ --", ""),
                    content=article.get("content", "").replace("/PRNewswire/ --", ""),
                    video_url=article.get("video_url"),
                    image_url=article.get("image_url"),
                    country=", ".join(article.get("country", "")),
                    language=article.get("language", ""),
                    published_at=article.get("pubDate"),
                )
                categories = article.get("category", "")
                for category in categories:
                    cate = Category.objects.get_or_create(
                        name=category,
                        slug=slugify(category),
                    )
                    article_obj.save()
                    article_obj.category.add(cate[0])
                    article_obj.content = "".join(
                        [f"<p>{i}.</p>" for i in article_obj.content.split(". ")]
                    )
                    article_obj.save()
                count += 1
            except Exception as e:
                pass
        return count


url = "https://newsdata.io/api/1/news?apikey=pub_2014607f2e3972fa2475d0757936e8666bb78&q=technology&from_date=2023-04-10&to_date=2023-04-11"  # &page=1681266503d101e303c726f02a0f29fad8934599d8"
