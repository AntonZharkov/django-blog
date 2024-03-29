from actions.models import LikeDislike
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy
from taggit.managers import TaggableManager

from .choices import ArticleStatus

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("-id",)

    def save(self, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwargs)


class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="article_set"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="article_set"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(
        choices=ArticleStatus.choices, default=ArticleStatus.INACTIVE
    )
    image = models.ImageField(
        upload_to="articles/", blank=True, default="no-image-available.jpg"
    )
    objects = models.Manager()
    votes = GenericRelation(LikeDislike, related_query_name="articles")
    tags = TaggableManager()

    @property
    def short_title(self):
        return self.title[:30]

    def __str__(self):
        return "{title} - {author}".format(title=self.short_title, author=self.author)

    def save(self, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(**kwargs)

    def get_absolute_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-updated", "-created", "id")


class Comment(models.Model):
    author = models.EmailField()
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comment_set",
        blank=True,
    )
    content = models.TextField(max_length=200)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comment_set"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    votes = GenericRelation(LikeDislike, related_query_name="comments")

    objects = models.Manager()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
