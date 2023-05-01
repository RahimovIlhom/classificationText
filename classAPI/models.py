from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Field(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=250, blank=True, null=True)
    body = RichTextField()
    photo = models.ImageField(upload_to='images', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    field = models.ForeignKey(
        Field,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # agar ssilka yoki boshlig'iga o'tkazilishida, qolgan yozuvni bo'shatish
        related_name='posts'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=250)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
