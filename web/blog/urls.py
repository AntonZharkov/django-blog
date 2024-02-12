from django.urls import path
from main.views import TemplateAPIView
from rest_framework.routers import DefaultRouter

from . import views

app_name = "blog"

urlpatterns = [
    path(
        "blog/",
        TemplateAPIView.as_view(template_name="blog/post_list.html"),
        name="blog-list",
    ),
    path(
        "blog/<slug:slug>/",
        TemplateAPIView.as_view(template_name="blog/post_detail.html"),
        name="post-detail",
    ),
    path(
        "create/",
        TemplateAPIView.as_view(template_name="blog/create_article.html"),
        name="create-article",
    ),
]
