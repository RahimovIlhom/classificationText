from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .classPost.classificationText import checkText
from .models import Post, Comment, Field
from .pagination import CustomPagination
from .serializers import CommentSerializers, PostSerializers, FieldSerializers


class FieldViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Field.objects.all()
        page = CustomPagination
        serializers = FieldSerializers(queryset, many=True, context=self.get_serializers_context())
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        queryset = Field.objects.all()
        page = CustomPagination
        field = get_object_or_404(queryset, pk=pk)
        serilizers = FieldSerializers(field, context=self.get_serializers_context())
        return Response(serilizers.data)

    def create(self, request):
        author = request.user
        field = Field.objects.create(
            author=author,
        )
        serializer = FieldSerializers(field, data=request.data, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializers_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action == 'list':
            permission_class = [IsAuthenticated]
        else:
            permission_class = [IsAdminUser]
        return [permission() for permission in permission_class]


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        page = CustomPagination
        serializers = PostSerializers(queryset, many=True, context=self.get_serializers_context())
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        page = CustomPagination
        post = get_object_or_404(queryset, pk=pk)
        serilizers = PostSerializers(post, context=self.get_serializers_context())
        return Response(serilizers.data)

    def create(self, request, *args, **kwargs):
        author = request.user
        fields = Field.objects.all()
        postNew = Post.objects.create(author=author)
        serializer = PostSerializers(postNew, data=request.data, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            postNew.body = serializer.validated_data['body']
            postNew.title = serializer.validated_data['title']
            try:
                postNew.summary = serializer.validated_data['summary']
                text = postNew.body + " " + postNew.title + " " + postNew.summary
            except:
                text = postNew.body + " " + postNew.title
            field = checkText(text.lower())['label']
            print(field)
            field_id = None
            for soha in fields:
                if soha.title.lower() == field.lower():
                    field_id = soha.id
                    break
            if field_id is None:
                return Response({"detail": "Bu post bazadagi sohalarga tegishli emas."},
                                status=status.HTTP_400_BAD_REQUEST)
            postNew.field_id = field_id
            postNew.save()
            serializer = PostSerializers(postNew, context=self.get_serializers_context())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializers(post, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializers(post, partial=True, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializers_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_class = [IsAuthenticated]
        else:
            permission_class = [IsAdminUser]
        return [permission() for permission in permission_class]


class CommentViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Comment.objects.all()
        page = CustomPagination
        serializers = CommentSerializers(queryset, many=True, context=self.get_serializers_context())
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        page = CustomPagination
        comment = get_object_or_404(queryset, pk=pk)
        serilizers = CommentSerializers(comment, context=self.get_serializers_context())
        return Response(serilizers.data)

    def create(self, request, *args, **kwargs):
        author = request.user
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        commentNew = Comment.objects.create(
            author=author,
            post=post
        )
        serializer = CommentSerializers(commentNew, data=request.data, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializers(comment, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializers(comment, partial=True, context=self.get_serializers_context())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializers_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_class = [IsAuthenticated]
        else:
            permission_class = [IsAdminUser]
        return [permission() for permission in permission_class]
