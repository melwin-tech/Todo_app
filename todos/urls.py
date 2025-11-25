from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('signout/', signout, name="signout"),
    path('create/', create_todo, name="create_todo"),
    path("edit/<int:id>/", edit_todo, name="edit_todo"),
    path("delete/<int:id>/", delete_todo, name="delete_todo")
]
