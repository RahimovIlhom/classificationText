from rest_framework import routers
from accounts.views import UserViewSet
from classAPI.views import FieldViewSet, PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
