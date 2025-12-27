from django.urls import path
from .views import KeyboardListCreateView

urlpatterns = [
    path('keyboards/', KeyboardListCreateView.as_view(), name="keyboard-list-create"),
]