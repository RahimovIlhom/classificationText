from django.urls import path
from .views import CustomRegisterView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='signup'),
]
