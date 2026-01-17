from django.urls import path
from .views import KeyboardListCreateView, KeyboardDetailView

urlpatterns = [
    path('keyboards/', KeyboardListCreateView.as_view(), name="keyboard-list-create"),
    path('keyboards/<int:pk>/', KeyboardDetailView.as_view(), name="keyboard-detail"),
]