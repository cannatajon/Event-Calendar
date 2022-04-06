
import json
import calendar
import os
import requests
import uuid
import boto3
from urllib import response

from getpass import getuser
from socket import create_server
from urllib import request, response

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import EventForm

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from webbrowser import get

# we import these to secure the url paths
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# and we write these to secure them :
# @login_required above functions as a decoration and
# LoginRequiredMixin i.e somethingUpdate(LoginRequiredMixin, UpdateView)

from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from django.db.models import Q
from .models import *

from .utils import Calendar
from django.views.generic.edit import DeleteView, UpdateView


S3_BASE_URL = 'https://s3-ca-central-1.amazonaws.com/'
BUCKET = 'eventcalendar2'


@login_required
def home(req):
    return render(req, "home.html")


@login_required
def search(req):
    events = []
    cities = ["toronto", "montreal", "calgary", "ottawa", "edmonton",
              "mississauga", "winnipeg", "vancouver", "brampton", "quebec"]

    search_term = req.GET.get("q") if req.GET.get("q") else ""
    search_locations = req.GET.getlist(
        "cities") if req.GET.getlist("cities") else cities

    if len(search_term) > 0:
        events = Event.objects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(tags__name__icontains=search_term) |
            Q(venue__name__icontains=search_term) |
            Q(venue__address__icontains=search_term),
            Q(venue__city__in=search_locations)
        ).distinct()

    return render(req, "search.html", {
        "search_term": search_term,
        "search_locations": search_locations,
        "events": events[:20],
        "num_results": events.count
    })


def event_detail(request, event_id):
    detail_items = []
    e = Event.objects.get(id=event_id)
    user = request.user

    url = f"https://www.eventbriteapi.com/v3/events/{e.eventbrite_id}/structured_content/?purpose=listing"
    headers = {
        'Authorization': f"Bearer {os.getenv('EVENTBRITE_API_KEY')}"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    print(data)
    details = data['modules']
    for detail in details:
        try:
            detail_items.append(detail['data']['body']['text'])
        except KeyError:
            pass

    context = {'event': e, 'details': detail_items, 'user': user}
    return render(request, 'event_detail.html', context)


def add_to_calendar(request, event_id):
    e = Event.objects.get(id=event_id)

    if request.method == 'POST':
        e.attendees.add(request.user)
        return redirect('event_detail', e.id)

    return render(request, 'confirm_add_to_cal.html', {'event': e})


def remove_from_calendar(request, event_id):
    e = Event.objects.get(id=event_id)

    if request.method == 'POST':
        e.attendees.remove(request.user)
        return redirect('event_detail', e.id)

    return render(request, 'confirm_remove_from_cal.html', {'event': e})

# not sure if this willa ctually help but
# This can be used for later when we create an event view
# so whoever makes the event it will be stored as thier id in the database (we can use this for when we create the calander view as well):
# def form_valid(self, form):
#     form.instance.user = self.request.user
#     return super().form_valid(form)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('home')
        else:
            error_message = 'Uh Oh - Sign up failed - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def grid_view(req):
    return render(req, 'grid_view.html')


class Calendar(HTMLCalendar):
    def getUser(self, req):
        self.currentUser = getCurrentUser(req)
        return self.currentUser

    def __init__(self, year=None, month=None, user=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<a href="/events/{event.id}"><li> {event.title} </li></a>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        # print(self.request)
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month, attendees=self.user)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'grid_view.html'

    def get_context_data(self, **kwargs):
        currentUser = self.request.user
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        user = self.request.user
        cal = Calendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['event_list'] = []
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def about(request):
    return render(request, "about.html")


def profile(request):
    user = request.user
    myEvents = Event.objects.filter(created_by=request.user)
    allEvents = Event.objects.filter(attendees=request.user)
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'user': user, 'my_events': myEvents, 'all_events': allEvents})


def add_photo(request, profile_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            profile = Profile.objects.get(id=profile_id)
            profile.profile_pic = url
            profile.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile')


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'


class editProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['profile_pic', 'bio']
    success_url = '/profile/'


def event_create(req):
    event_form = EventForm()
    return render(req, 'create_event.html', {'event_form': event_form})


def add_event(req):
    form = EventForm(req.POST)
    if form.is_valid():
        new_event = form.save(commit=False)
        new_event.created_by = req.user
        new_event.save()
        new_event.attendees.add(req.user)
    return redirect('grid_view')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)
