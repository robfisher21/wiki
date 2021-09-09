from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search.html",views.search, name="search"),
    path("article/<str:title>",views.title, name="title"),
    path("add.html",views.add, name="add"),
    path("edit.html",views.edit, name="edit"),
    path("random.html",views.random, name="random"),
    
]
