from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    

    #For Django Auth
    path('accounts/signup/', views.signup, name='signup'),
    path('gridview/', views.CalendarView.as_view(), name='grid_view'),s
]

