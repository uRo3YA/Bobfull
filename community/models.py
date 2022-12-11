from django.db import models
from accounts.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    created_at = models.DateTimeField('생성시간', auto_now_add=True)
    modified_at = models.DateTimeField('수정시간', auto_now=True)
    like = models.ManyToManyField(User, related_name="article_like")

    class Meta:
        ordering = ["-created_at"]

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField('생성시간', auto_now_add=True)

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="like_articles"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like"
    )

class ReComment(models.Model):
    article = models.ForeignKey(
        Article,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="recomments",
    )
    user = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        Comment,
        related_name="soncomments",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content = models.TextField()

    def __str__(self):
        return self.content