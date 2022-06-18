from django.urls import path
from mind_map import views

urlpatterns = [
    path('', views.index, name="mind_map")
]