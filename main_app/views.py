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

# Create your views here.


def home(req):
    return render(req, "home.html")


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