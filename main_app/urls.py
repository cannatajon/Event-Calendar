from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gridview/', views.CalendarView.as_view(), name='grid_view'),
    path('search/', views.search, name='search'),

    path('events/create', views.event_create, name="event_create"),
    path('events/<int:event_id>', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/addtocalendar',
         views.add_to_calendar, name='add_to_calendar'),
    path('events/addevent', views.add_event, name='add_event'),

    # For Django Auth
    path('accounts/signup/', views.signup, name='signup'),

]
