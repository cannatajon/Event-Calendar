from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gridview/', views.CalendarView.as_view(), name='grid_view'),
    path('search/', views.search, name='search'),
]
