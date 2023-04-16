from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Articles Category table
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("category name"),
        help_text=_("format: required, max-100"),
        db_index=True,
        unique=True,
    )
    slug = models.SlugField(
        max_length=150,
        verbose_name=_("The category slug to form URL."),
        help_text=_("format: required, letters, numbers, underscore, or hyphens"),
        unique=True,
    )

    class Meta:
        verbose_name = _("article category")
        verbose_name_plural = _("article categories")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(
        max_length=255, verbose_name=_("Article Title"), db_index=True, unique=True
    )
    meta_title = models.CharField(
        max_length=255,
        verbose_name=_("Meta Title"),
        help_text=_("The meta title to be used for browser title and SEO."),
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name=_("Slug"),
        help_text=_("The article slug to form URL."),
        unique=True,
    )
    category = models.ManyToManyField(Category, related_name="categories")
    description = models.TextField(
        max_length=1015,
        verbose_name=_("Description"),
        help_text=_("The description of the article to mention the key highlights."),
    )
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=15, default="")
    language = models.CharField(max_length=15, default="")
    published_at = models.DateTimeField(
        default=now,
        verbose_name=_("Published At"),
        help_text=_("It stores the date and time at which the article is Published."),
    )
    reading_times = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Reading Times"),
        help_text=_("Increasing positive number to calculate the reading times."),
    )
    trending = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Trending"),
        help_text=_("Increasing positive number to calculate the reading times."),
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article", args=[self.slug])

    def plus_one(self, request):
        if request.session.get("ids") is None:
            request.session["ids"] = []

        if not self.id in request.session["ids"]:
            self.reading_times = F("reading_times") + 1
            self.trending = F("trending") + 1
            self.save()
            request.session["ids"].append(self.id)


class ArticleMeta(models.Model):
    """
    The Article Meta Table can be used to store additional information of a article
    including the article banner URL etc.
    """

    article = models.OneToOneField(Article, on_delete=models.CASCADE, unique=True)
    key = models.CharField(
        max_length=50, verbose_name=_("Key"), help_text=_("The key identifying the meta.")
    )
    content = models.TextField(
        verbose_name=_("Key"), help_text=_("The column used to store the article data.")
    )

    def __str__(self):
        return self.article.title
