from .models import User, Club
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .forms import UserForm#, TutorForm, ClubForm, CourseForm
from django.views.generic import ListView, FormView, DetailView


def homepage(request):
    Clubs = Club.objects.all()
    return render(request, "home.html", {"Clubs": Clubs})

def link(request):
    return render(request, "link.html")

def Register(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            
    
    return render(request, "log_up.html", {"form": form})
    
    