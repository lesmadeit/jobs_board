from django.shortcuts import render, get_object_or_404, redirect
from jobs.models import CompanyProfile, Application, Job, Message, ResponseTemplate
from django.http import Http404, HttpResponseForbidden, FileResponse
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from jobs.forms import JobForm, MessageForm, ResponseTemplateForm
from django.contrib import messages

from jobs.views import is_employer


@user_passes_test(is_employer)
def dashboard_summary(request):
    try:
        company = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return HttpResponseForbidden("Company profile not found. Please set up your company profile.")
    

    #Calculate overview stats
    employer_jobs = Job.objects.filter(company=company)
    total_jobs = employer_jobs.count()
    total_applicants = Application.objects.filter(job__company=company).values('applicant').distinct().count()
    applications = Application.objects.filter(job__company=company).aggregate(
        total=Count('id'),
        jobs=Count('job', distinct=True)

    )
    avg_applications = (
        round(applications['total'] / applications['jobs'], 1)
        if applications['jobs'] > 0 else 0
    )

    context = {
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'avg_applications': avg_applications,
    }
    return render(request, 'dashboard/summary.html', context)



@user_passes_test(is_employer)
def job_listings_management(request):
    # Get the employer's company profile
    try:
        company = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return HttpResponseForbidden("Company profile not found. Please set up your company profile.")

    # Job listings data
    job_listings = Job.objects.filter(company=company).annotate(
        applicant_count=Count('applications', distinct=True),
    ).order_by('-created_at')

    # Determine status for each job
    current_date = timezone.now().date()
    for job in job_listings:
        if not job.is_public:
            job.status = 'draft'
        elif job.application_deadline and job.application_deadline < current_date:
            job.status = 'expired'
        else:
            job.status = 'active'

    context = {
        'job_listings': job_listings,
    }
    return render(request, 'dashboard/job_listings.html', context)




@user_passes_test(is_employer)
def edit_job(request, pk):
    """
    Allow an employer to update a job posting that they own.
    """
    job = get_object_or_404(Job, pk=pk, company__user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard:job_listings_management',)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})



@user_passes_test(is_employer)
def close_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)
    job.is_public = False
    job.save()
    return redirect('dashboard:dashboard_summary')



@user_passes_test(is_employer)
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)

    if request.method == 'POST':
        job.delete()
        messages.success(request, f'Job "{job.title}" has been deleted.')
        return redirect('dashboard:job_listings_management')
    return render(request, 'dashboard/confirm_delete_job.html', {'job': job})



@user_passes_test(is_employer)
def applicants_management(request, pk):
    try:
        company = request.user.company_profile
    except CompanyProfile.DoesNotExist:
        return HttpResponseForbidden("Company profile not found. Please set up your company profile.")
    
    # Get the specific job, ensuring it belongs to the employer
    job = get_object_or_404(Job, pk=pk, company=company)

    # Get all applications for this job
    applications = Application.objects.filter(job=job).select_related('applicant')

    # Filtering logic
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')


    if status_filter:
        applications = applications.filter(status=status_filter)
    if search_query:
        applications = applications.filter(
            Q(applicant__username__icontains=search_query) |
            Q(cover_letter__icontains=search_query)
        )

    context = {
        'job': job,
        'applications': applications,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'dashboard/applicants_management.html', context)


# Action views
@user_passes_test(is_employer)
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)
    # Ensure the application belongs to the employer's job
    if application.job.company != request.user.company_profile:
        return HttpResponseForbidden("You don't have permission to modify this application.")
    
    application.status = status
    application.save()
    return redirect('dashboard:applicants_management', pk=application.job.id)



@user_passes_test(is_employer)
def download_resume(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    # Ensure the resume belongs to the employer's job
    if application.job.company != request.user.company_profile:
        return HttpResponseForbidden("You don't have permission to access this resume.")
    
    resume_file = application.resume
    response = FileResponse(resume_file.open(), as_attachment=True, filename=resume_file.name.split('/')[-1])
    return response
    


@user_passes_test(is_employer)
def message_inbox(request):
    company = request.user.company_profile
    messages_list = Message.objects.filter(recipient_company=company, parent_message__isnull=True)
    unread_count = messages_list.filter(is_read=False).count()

    # Mark messages as read when viewed (optional, can be triggered by clicking a message)
    if request.GET.get('mark_read'):
        message_id = request.GET.get('mark_read')
        message = get_object_or_404(Message, id=message_id, recipient_company=company)
        message.is_read = True
        message.save()
    
    context = {
        'message': messages_list,
        'unread_count': unread_count,
    }
    return render(request, 'dashboard/message_inbox.html', context)


@user_passes_test(is_employer)
def reply_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id, recipient_company=request.user.company_profile)
    company = request.user.company_profile

    if request.method == 'POST':
        form = MessageForm(request.POST)
        template_id = request.POST.get('template')
        if template_id:
            template = get_object_or_404(ResponseTemplate, id=template_id, company=company)
            form = MessageForm(initial={'subject': f"Re: {original_message.subject}", 'body': template.content})

        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient_company = original_message.sender.profile.company_profile if original_message.sender.profile.user_type == 'employer' else None
            reply.job = original_message.job
            reply.parent_message = original_message
            reply.save()
            original_message.is_read = True
            original_message.is_read.save()
            messages.success(request, "Reply sent successfully.")
            return redirect('dashboard:message_inbox')
    else:
        form = MessageForm(initial={'subject': f"Re: {original_message.subject}"})

    templates = ResponseTemplate.objects.filter(company=company)
    context = {
        'forms': form,
        'original_message': original_message,
        'templates': templates,
    }
    return render(request, 'dashboard/reply_message.html', context)


@user_passes_test(is_employer)
def manage_response_templates(request):
    company = request.user.company_profile
    templates = ResponseTemplate.objects.filter(company=company)

    if request.method == 'POST':
        form = ResponseTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.company = company
            template.save()
            messages.success(request, "Template created successfully")
            return redirect('dashboard:manage_response_templates')
    else:
        form = ResponseTemplateForm()
    
    context = {'form': form, 'templates': templates}
    return render(request, 'dashboard/response_templates.html', context)

