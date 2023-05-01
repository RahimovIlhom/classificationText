from rest_framework import serializers
from .models import Post, Comment, Field
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer


class FieldSerializers(serializers.ModelSerializer):
    # author = UserSerializer(
    #     many=False,
    #     required=False
    # )

    class Meta:
        model = Field
        fields = ['id', 'author_id', 'title', 'description', 'date', 'posts', 'url']
        write_only_fields = ['author_id']


class PostSerializers(serializers.ModelSerializer):
    # author = UserSerializer(
    #     many=False,
    #     required=False
    # )

    class Meta:
        model = Post
        fields = ['id', 'field_id', 'author_id', 'title', 'summary', 'photo', 'body', 'date', 'comments', 'url']
        write_only_fields = ['author_id', 'field_id']


class CommentSerializers(serializers.ModelSerializer):
    # post = PostSerializers(
    #     many=False,
    #     required=False
    # )
    # author = UserSerializer(
    #     many=False,
    #     required=False
    # )

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'author_id', 'post_id', 'created_at', 'url']
        write_only_fields = ['author_id', 'post_id']
