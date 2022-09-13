from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('rooms/', views.rooms, name="rooms"),
    path('rooms/<int:pk>', views.RoomsDetailView.as_view(), name='room-detail'),
]
