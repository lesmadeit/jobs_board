from django.shortcuts import render
from django.contrib import messages
from . import forms, models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, CompanyProfile, Application, Testimonial, JOB_TYPE_CHOICES, EXPERIENCE_LEVEL_CHOICES, POSTED_WITHIN_CHOICES, INDUSTRY_CHOICES
from .forms import CompanyProfileForm, JobForm, ApplicationForm, TestimonialForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils.timezone import now
from django.http import Http404, HttpResponseForbidden, FileResponse
from .models import BlogPost, BlogReply, BlogLike, BlogCategory
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from .forms import MessageForm



def home(request):
    featured_jobs = Job.objects.filter(featured=True, is_public=True).order_by('-created_at')[:5]  # Limit to 5
    testimonials = Testimonial.objects.all()
    recent_blogs = BlogPost.objects.order_by('-created_at')[:2]
    context ={
        'featured_jobs': featured_jobs,
        'testimonials': testimonials,
        'recent_blogs': recent_blogs,

    }
    return render(request, "jobs/home.html", context)


def about(request):
    testimonials = Testimonial.objects.all()
    recent_blogs = BlogPost.objects.order_by('-created_at')[:2]
    context = {
        'testimonials': testimonials,
        'recent_blogs': recent_blogs,
    }
    return render(request, "jobs/about.html", context)


def services(request):
    return render(request, "jobs/services.html")


def service_details(request):
    return render(request, "jobs/service_details.html")







def contact(request):
    if request.method == 'POST':
        form = forms.ContactusForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            name = form.cleaned_data['Name']
            message = form.cleaned_data['Message']
            send_mail(
                f"{name} || {email}",
                message,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECEIVING_USER,
                fail_silently=False
            )
            return render(request, "jobs/contactussuccess.html")
    else:
        form = forms.ContactusForm()
    
    return render(request, "jobs/contact_us.html", {'form': form})


def job_list(request):
    jobs = Job.objects.filter(is_public=True).order_by('-created_at')

    if request.user.is_authenticated and hasattr(request.user, 'company_profile'):
        jobs = Job.objects.filter(company=request.user.company_profile).order_by('-created_at')

    # Apply filters
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query)

    job_type = request.GET.getlist('job_type')
    if job_type:
        jobs = jobs.filter(job_type__in=job_type)

    experience_level = request.GET.getlist('experience_level')
    if experience_level:
        jobs = jobs.filter(experience_level__in=experience_level)

    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)


    industry = request.GET.get('industry')
    if industry and industry != 'all':  # 'all' represents "All Category"
        jobs = jobs.filter(industry=industry)

    # Filter by "posted within"
    posted_within = request.GET.get('posted_within', 'any')  # Default to "any"
    if posted_within.isdigit():  # Ensure it's a valid number
        days = int(posted_within)
        jobs = jobs.filter(created_at__gte=now() - timedelta(days=days))

    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'job_type_choices': JOB_TYPE_CHOICES,
        'selected_job_types': job_type,
        'experience_level_choices': EXPERIENCE_LEVEL_CHOICES,
        'selected_experience_levels': experience_level,
        'posted_within_choices': POSTED_WITHIN_CHOICES,
        'selected_posted_within': posted_within,
        'industry_choices': INDUSTRY_CHOICES,  
        'selected_industry': industry or 'all', # Default to 'all' if no industry selected
    })


def featured_jobs(request):
    featured_jobs = Job.objects.filter(featured=True, is_public=True).order_by('-created_at')
    return render(request, 'jobs/featured_jobs.html', {'featured_jobs': featured_jobs})



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
        return redirect('jobs:company_profile_create')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company_profile
            job.save()
            return redirect('jobs:job_detail', pk=job.pk)
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
            return redirect('jobs:job_detail', pk=job.pk)
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
            return redirect('jobs:job_detail', pk=pk)
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been sent successfully!")
            return HttpResponseRedirect('jobs:apply_job', pk=pk)
              
 

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
        return redirect('jobs:company_profile_view')
    except CompanyProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('jobs:company_profile_view')  # or your dashboard
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
            return redirect('jobs:company_profile_view')  # or your dashboard
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



@login_required
@user_passes_test(is_employer)
def add_testimonial(request):
    if not hasattr(request.user, 'company_profile') or request.user.profile.user_type != 'employer':
        return redirect('home')  # Redirect non-employers
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.company = request.user.company_profile  # Link to the employer’s company profile
            testimonial.save()
            return redirect('jobs:testimonial_list')
    else:
        form = TestimonialForm()
    return render(request, 'jobs/add_testimonial.html', {'form': form})

@login_required
@user_passes_test(is_employer)
def edit_testimonial(request, pk):
    if not hasattr(request.user, 'company_profile') or request.user.profile.user_type != 'employer':
        raise Http404
    testimonial = get_object_or_404(Testimonial, pk=pk, company=request.user.company_profile)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            return redirect('jobs:testimonial_list')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'jobs/edit_testimonial.html', {'form': form, 'testimonial': testimonial})


@login_required
@user_passes_test(is_employer)
def delete_testimonial(request, pk):
    if not hasattr(request.user, 'company_profile') or request.user.profile.user_type != 'employer':
        raise Http404
    testimonial = get_object_or_404(Testimonial, pk=pk, company=request.user.company_profile)
    if request.method == 'POST':
        testimonial.delete()
        return redirect('jobs:testimonial_list')
    return render(request, 'jobs/delete_testimonial.html', {'testimonial': testimonial})


@login_required
@user_passes_test(is_employer)
def testimonial_list(request):
    if request.user.is_authenticated and hasattr(request.user, 'company_profile') and request.user.profile.user_type == 'employer':
        testimonials = Testimonial.objects.filter(company=request.user.company_profile).order_by('-created_at')
    else:
        testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'jobs/testimonial_list.html', {'testimonials': testimonials})




def blog_list(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')

    # Search filter
    query = request.GET.get('q')
    if query:
        blog_posts = blog_posts.filter(title__icontains=query) | blog_posts.filter(content__icontains=query)

    # Category filter
    category = request.GET.get('category')
    if category:
        blog_posts = blog_posts.filter(category__name=category)

    paginator = Paginator(blog_posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    categories = BlogCategory.objects.all()
    recent_posts = BlogPost.objects.order_by('-created_at')[:4]

    return render(request, 'jobs/blog_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'recent_posts': recent_posts,
    })

def blog_detail(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)

    # Previous and next posts
    previous_post = BlogPost.objects.filter(created_at__lt=blog_post.created_at).order_by('-created_at').first()
    next_post = BlogPost.objects.filter(created_at__gt=blog_post.created_at).order_by('created_at').first()

    # Sidebar data
    categories = BlogCategory.objects.all()
    recent_posts = BlogPost.objects.order_by('-created_at')[:4]

    context = {
        'blog_post': blog_post,
        'previous_post': previous_post,
        'next_post': next_post,
        'categories': categories,
        'recent_posts': recent_posts,
    }
    return render(request, 'jobs/blog_details.html', context)


@login_required
def add_reply(request, blog_id, parent_id=None):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    parent_reply = None
    if parent_id:
        parent_reply = get_object_or_404(BlogReply, id=parent_id, blog_post=blog_post)

    if request.method == 'POST':
        content = request.POST.get('comment')
        if content:
            BlogReply.objects.create(
                blog_post=blog_post,
                author=request.user,
                content=content,
                parent=parent_reply  # Set parent if replying to a reply
            )
        return redirect('jobs:blog_detail', blog_id=blog_id)

    return redirect('jobs:blog_detail', blog_id=blog_id)  # Fallback for GET requests

@login_required
def delete_reply(request, blog_id, reply_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    reply = get_object_or_404(BlogReply, id=reply_id, blog_post=blog_post)
    
    # Check if the logged-in user is the author of the reply
    if reply.author != request.user:
        raise Http404("You are not authorized to delete this reply.")
    
    if request.method == 'POST':
        reply.delete()
        return redirect('jobs:blog_detail', blog_id=blog_id)
    
    # Optional: Show a confirmation page for GET requests
    return render(request, 'jobs/delete_reply_confirm.html', {
        'reply': reply,
        'blog_post': blog_post,
    })



@login_required
def toggle_like(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    like, created = BlogLike.objects.get_or_create(blog_post=blog_post, user=request.user)
    if not created:  # If like exists, remove it
        like.delete()
    return redirect('jobs:blog_detail', blog_id=blog_id)


@login_required
def send_message(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    if request.user.profile.user_type != 'candidate':
        messages.error(request, "Only candidates can send messages.")
        return redirect('jobs:jobs')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, company=company)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient_company = company
            message.save()
            message.save()
            messages.success(request, "Your message has been sent.")
            return redirect('jobs:jobs')
    else:
        form = MessageForm(company=company)
    return render(request, 'jobs/send_message.html', {'form': form, 'company': company})
















