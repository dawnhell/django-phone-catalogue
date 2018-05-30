from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('phone/<int:phone_id>/', views.detail, name='detail'),
    path('search', views.search, name='search')
]
