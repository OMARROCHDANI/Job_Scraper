from django.urls import path,include
from . import views
urlpatterns = [
    path('' ,views.profile_create, name='profile_create' ),
]