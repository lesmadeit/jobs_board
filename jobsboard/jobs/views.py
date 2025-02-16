from django.shortcuts import render
from django.contrib import messages
from . import forms, models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, CompanyProfile, Application
from .forms import CompanyProfileForm, JobForm, ApplicationForm
from django.http import HttpResponseRedirect



def home(request):
    return render(request, "jobs/home.html")


def about(request):
    return render(request, "jobs/about.html")


def services(request):
    return render(request, "jobs/services.html")


def service_details(request):
    return render(request, "jobs/service_details.html")


def blog(request):
    return render(request, "jobs/blog.html")


def blog_details(request):
    return render(request, "jobs/blog_details.html")


def contact(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email), message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, "jobs/contactussuccess.html")
    return render(request, "jobs/contact_us.html", {'form':sub})



def job_list(request):
    """
    Display jobs based on the user type:
    - Employers see only their posted jobs.
    - Candidates see all public jobs.
    """
    jobs = Job.objects.filter(is_public=True).order_by('-created_at')  # Default: Show all public jobs

    if request.user.is_authenticated and hasattr(request.user, 'company_profile'):
        # If the user is an employer, show only their posted jobs
        jobs = Job.objects.filter(company=request.user.company_profile).order_by('-created_at')

    # Apply filters (for both candidates & employers)
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query)

    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'jobs/job_list.html', {'jobs': jobs})



def job_detail(request, pk):
    """
    Show full job details along with company info.
    """
    job = get_object_or_404(Job, pk=pk)
    context = {
        'job': job,
    }
    return render(request, 'jobs/job_detail.html', context)

def is_employer(user):
    return user.is_authenticated and user.profile.user_type == 'employer'

@login_required
@user_passes_test(is_employer)
def job_create(request):
    """
    Allow an employer (user with a company profile) to create a job.
    """
    try:
        company_profile = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return redirect('company_profile_create')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company_profile
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
@user_passes_test(is_employer)
def job_update(request, pk):
    """
    Allow an employer to update a job posting that they own.
    """
    job = get_object_or_404(Job, pk=pk, company__user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})



@login_required
def apply_job(request, pk):
    """
    Allow a logged-in user to apply for a job.
    """
    job = get_object_or_404(Job, pk=pk)

    
          
    
    if request.method == 'POST':
        # Check if the user has already applied to avoid duplicate application
        if Application.objects.filter(job=job, applicant=request.user).exists():
            messages.error(request, "You have already applied for this job.")
            return redirect('job_detail', pk=pk)
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been sent successfully!")
            return HttpResponseRedirect('apply_job', pk=pk)
              
 

    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})



@login_required
@user_passes_test(is_employer)
def view_applicants(request, pk):
    """
    Allow an employer to view and shortlist job applicants.
    """
    job = get_object_or_404(Job, pk=pk, company__user=request.user)
    applications = job.applications.all().order_by('-applied_at')
    return render(request, 'jobs/view_applicants.html', {'job': job, 'applications': applications})





@login_required
@user_passes_test(is_employer)
def company_profile_create(request):
    """
    Allow a user to create a company profile (for employers/recruiters).
    """
    try:
        # If already exists, redirect to edit page.
        request.user.company_profile
        return redirect('company_profile_view')
    except CompanyProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('company_profile_view')  # or your dashboard
    else:
        form = CompanyProfileForm()
    return render(request, 'jobs/company_profile_form.html', {'form': form})




@login_required
@user_passes_test(is_employer)
def company_profile_update(request):
    """
    Allow a user to update their company profile.
    """
    profile = get_object_or_404(CompanyProfile, user=request.user)
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('company_profile_view')  # or your dashboard
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'jobs/company_profile_form.html', {'form': form})


@login_required
@user_passes_test(is_employer)
def company_profile_view(request):
    """
    Display the company profile with an edit button.
    """
    profile = get_object_or_404(CompanyProfile, user=request.user)
    
    return render(request, 'jobs/view_company_profile.html', {'profile': profile})
