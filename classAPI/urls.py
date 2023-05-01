from django.urls import path
from classAPI.views import CommentViewSet

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({'post': 'create'})),
]