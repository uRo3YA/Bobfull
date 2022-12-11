from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.ArticleViewSet, basename="article")

urlpatterns = [
    path('', include(router.urls)),
    path("<int:article_pk>/", views.ArticleViewSet),
    path(
        "<int:article_pk>/comment/",
        views.CommentViewSet.as_view({"post": "create", "get": "list"}),
    ),
    path(
        "<int:article_pk>/comment/<int:pk>/",
        views.CommentViewSet.as_view(
            {"put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path(
        "<int:article_pk>/comment/<int:comment_pk>/recomment/",
        views.ReCommentViewSet.as_view({"post": "create", "get": "list"}),
    ),
    # 수정
    path(
        "<int:article_pk>/comment/<int:comment_pk>/recomment/<int:pk>",
        views.ReCommentViewSet.as_view(
            {"put": "update", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path(
        "<int:article_pk>/like/",
        views.LikeCreate.as_view(),
    ),
]