from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gridview/', views.CalendarView.as_view(), name='grid_view'),
    path('search/', views.search, name='search'),
    path('events/create', views.EventCreate.as_view(), name = "event_create" ),
 #For Django Auth
    path('accounts/signup/', views.signup, name='signup'),

]

