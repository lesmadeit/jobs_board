from django.shortcuts import render




def home(request):
    return render(request, "jobsapp/home.html")
