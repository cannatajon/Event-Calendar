from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gridview/', views.CalendarView.as_view(), name='grid_view'),
    path('search/', views.search, name='search'),

    path('events/create', views.EventCreate.as_view(), name="event_create"),
    path('events/<int:event_id>', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/addtocalendar', views.add_to_calendar, name='add_to_calendar'),

    # For Django Auth
    path('accounts/signup/', views.signup, name='signup'),

    #profile page urls
    path('profile/',views.profile, name='profile'),
    path('profile/<int:pk>/delete/', views.DeleteUser.as_view(), name = 'user_delete'),
    path('profile/<int:pk>/update/', views.editProfile.as_view(), name = 'edit_profile'),

]
