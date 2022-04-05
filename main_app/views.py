
import calendar
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


# Create your views here.
currentUser = None


def home(req):
    return render(req, "home.html")


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

    e = Event.objects.get(id=event_id)

    return render(request, 'event_detail.html', {'event': e})


def add_to_calendar(request, event_id):
    e = Event.objects.get(id=event_id)

    if request.method == 'POST':
        e.attendees.add(request.user.id)
        return redirect('event_detail', e.id)

    return render(request, 'confirm_add_to_cal.html', {'event': e})

    return

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
            return redirect('home')
        else:
            error_message = 'Uh Oh - Sign up failed - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


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
            d += f'<li> {event.title} </li>'

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
            start_time__year=self.year, start_time__month=self.month, created_by=self.user)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


class CalendarView(generic.ListView):
    model = Event
    template_name = 'grid_view.html'

    def get_context_data(self, **kwargs):
        currentUser = self.request.user
        context = super().get_context_data(**kwargs)

        newArr = []
        for i in context['event_list']:
            if i.created_by == self.request.user:
                newArr.append(i)

        context['object_list'] = newArr

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


def event_create(req):
    event_form = EventForm()
    return render(req, 'create_event.html', {'event_form': event_form})


def add_event(req):
    form = EventForm(req.POST)
    if form.is_valid():
        new_event = form.save(commit=False)
        new_event.created_by = req.user
        new_event.save()
    return redirect('grid_view')


def getCurrentUser(req):
    return req.user
