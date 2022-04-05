
import calendar
from urllib import response
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

#we import these to secure the url paths
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
 #and we write these to secure them : 
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



# Create your views here.

@login_required
def home(req):
    return render(req, "home.html")

@login_required
def search(req):
    events = []
    cities = ["toronto", "montreal", "calgary", "ottawa", "edmonton",
              "mississauga", "winnipeg", "vancouver", "brampton", "quebec"]

    search_term = req.GET.get("q") if req.GET.get("q") else ""
    search_locations = req.GET.getlist("cities") if req.GET.getlist("cities") else cities

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

@login_required
def grid_view(req):
    return render(req, 'grid_view.html')


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'grid_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
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