from django.shortcuts import render
from .models import Job
from .forms import JobSearchForm




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

def job_list(request):
    form = JobSearchForm(request.GET or None)
    jobs = Job.objects.all()

    if form.is_valid():
        if form.cleaned_data.get('keyword'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['keyword'])
        if form.cleaned_data.get('job_type'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['job_type'])
        if form.cleaned_data.get('location'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['location'])
        if form.cleaned_data.get('industry'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['industry'])
        if form.cleaned_data.get('experience_level'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['experience_level'])
        if form.cleaned_data.get('min_salary'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['min_salary'])
        if form.cleaned_data.get('max_salary'):
            jobs = jobs.filter(title__icontains=form.cleaned_data['max_salary'])

    return render(request, 'jobsapp/jobs_list.html', {'form': form, 'jobs': jobs})

        





