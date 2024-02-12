from actions.models import LikeDislike
from api.v1.blog.filters import ArticleFilter
from api.v1.blog.serializers import (ArticleCreateSerializer,
                                     CategorySerializer,
                                     CommentCreateSerializer,
                                     CommentSerializer, FullArticleSerializer,
                                     TagListSerializer)
from api.v1.blog.services import (BlogService, CreateArticleService,
                                  CreateCommentService,
                                  EmailCreateArticleAdminHandler,
                                  EmailCreateArticleUserHandler)
from blog.models import Article, Category, Comment
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, OuterRef, Prefetch, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from main.pagination import BasePageNumberPagination
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from taggit.models import Tag


class ArticleListView(GenericAPIView):
    serializer_class = FullArticleSerializer
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    # TODO: перенести запросы в сервис
    def get_queryset(self):
        count_comment_subquery = (
            Comment.objects.filter(article=OuterRef("id"))
            .values("article")
            .annotate(count_article=Count("content"))
            .values("count_article")
        )
        sum_like_dislike_subquery = (
            LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(Article),
                object_id=OuterRef("id"),
            )
            .values("object_id")
            .annotate(sum_like_dislike=Sum("vote"))
            .values("sum_like_dislike")
        )
        queryset = (
            Article.objects.select_related("category", "author")
            .prefetch_related("tags", "votes")
            .all()
            .annotate(
                comments_count=Coalesce(Subquery(count_comment_subquery), 0),
                count_like_dislike=Subquery(sum_like_dislike_subquery),
            )
            .order_by("created")
        )
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)


class ArticleDetailView(GenericAPIView):
    serializer_class = FullArticleSerializer
    # TODO:  изменить доступ на удаление и апдейт
    permission_classes = (AllowAny,)

    # TODO: перенести запросы в сервис
    def get_queryset(self):
        count_comment_subquery = (
            Comment.objects.filter(article=OuterRef("id"))
            .values("article")
            .annotate(count_article=Count("content"))
            .values("count_article")
        )
        sum_like_dislike_subquery = (
            LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(Article),
                object_id=OuterRef("id"),
            )
            .values("object_id")
            .annotate(sum_like_dislike=Sum("vote"))
            .values("sum_like_dislike")
        )
        return (
            Article.objects.select_related("category", "author")
            .prefetch_related("tags", "votes")
            .all()
            .annotate(
                comments_count=Coalesce(Subquery(count_comment_subquery), 0),
                count_like_dislike=Subquery(sum_like_dislike_subquery),
            )
            .order_by("created")
        )

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(slug=self.kwargs["slug"])

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class ArticleCreateView(GenericAPIView):
    serializer_class = ArticleCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_create = CreateArticleService()
        article = service_create.create_article(
            data=serializer.validated_data, user=request.user
        )

        service_email_admin = EmailCreateArticleAdminHandler(
            data=article, request=request
        )
        service_email_admin.send_email()

        service_email_user = EmailCreateArticleUserHandler(user=article.author.email)
        service_email_user.send_email()

        return Response(
            {"detail": _("The article has been sent to moderate")},
            status=status.HTTP_200_OK,
        )


class CategoryListView(GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagListView(GenericAPIView):
    serializer_class = TagListSerializer
    permission_classes = (AllowAny,)  #  изменить доступ на удаление и апдейт

    def get_queryset(self):
        return Tag.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentListView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination

    # TODO: возможно нужно перенести в сервис
    def get_queryset(self):
        sum_like_dislike_subquery = (
            LikeDislike.objects.filter(content_type=13, object_id=OuterRef("id"))
            .values("object_id")
            .annotate(count_like=Sum("vote"))
            .values("count_like")
        )

        children_prefetch_subquery = (
            Comment.objects.filter(
                article__slug=self.kwargs["article_slug"], parent__isnull=False
            )
            .annotate(count_like=Coalesce(Subquery(sum_like_dislike_subquery), 0))
            .prefetch_related("votes")
            .order_by("-updated")
        )

        return (
            Comment.objects.filter(
                article__slug=self.kwargs["article_slug"], parent__isnull=True
            )
            .annotate(count_like=Coalesce(Subquery(sum_like_dislike_subquery), 0))
            .prefetch_related(
                "votes", Prefetch("children", queryset=children_prefetch_subquery)
            )
            .order_by("-updated")
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class CommentCreateView(GenericAPIView):
    serializer_class = CommentCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CreateCommentService()
        service.create_comment(data=serializer.validated_data, user=request.user)

        return Response(
            {"detail": _("The comment has been created")},
            status=status.HTTP_201_CREATED,
        )
