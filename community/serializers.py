from pickletools import read_long1
from rest_framework import serializers

from accounts.serializers import CustomUserDetailsSerializer
from .models import Article, Comment, Like, ReComment

class ReCommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    parent = serializers.ReadOnlyField(source="parent.pk")
    article = serializers.ReadOnlyField(source="article.pk")

    class Meta:
        model = ReComment
        fields = [
            "pk",
            "article",
            "parent",
            "user",
            "content",
            "created_at",
        ]

class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailsSerializer(read_only=True)
    userpk = serializers.ReadOnlyField(source="user.pk")
    article = serializers.ReadOnlyField(source="article.pk")
    soncomments = ReCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "pk",
            "article",
            "user",
            "userpk",
            "content",
            "created_at",
            "soncomments",
        ]


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField(read_only=True)
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            "pk",
            "title",
            "content",
            "comments",
            "total_likes",
            "user",
            "created_at",
        ]

    def get_total_likes(self, article):
        return article.like.count()

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.nickname")
    article = serializers.ReadOnlyField(source="article.pk")

    class Meta:
        model = Like
        fields = [
            "pk",
            "user",
            "article",
        ]