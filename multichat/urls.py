from django.urls import path
from . import views

app_name = 'multichat'

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:room_pk>/send/", views.send, name="send"),
    path("<int:matchingroom_pk>/create/", views.create, name='create'),
    path("<int:matchingroom_pk>/join/", views.join, name='join'),
    path("<int:room_pk>/", views.detail, name="detail"),
    path('<int:room_pk>/finish/', views.finish, name='finish'),
]