from django.shortcuts import render




def home(request):
    return render(request, "jobsapp/home.html")

def about(request):
    return render(request, "jobsapp/about.html")

def services(request):
    return render(request, "jobsapp/services.html")


def service_details(request):
    return render(request, "jobsapp/service_details.html")

def contact(request):
    return render(request, "jobsapp/contact_us.html")



