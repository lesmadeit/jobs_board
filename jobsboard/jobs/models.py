from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


JOB_TYPE_CHOICES = (
    ('full_time', 'Full-Time'),
    ('part_time', 'Part-Time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
    ('temporary', 'Temporary'),
)

EXPERIENCE_LEVEL_CHOICES = (
    ('intern', 'Intern'),
    ('junior', 'Junior'),
    ('intermediate', 'Intermediate'),
    ('senior', 'Senior'),
)

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True)  
    website = models.URLField(blank=True)
    email = models.EmailField(
        max_length=255,
        blank=True,
        validators=[EmailValidator(message="Enter a valid email address")]
    )
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.company_name
    

class Job(models.Model):
    company = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    salary_min = models.PositiveIntegerField( null=True, blank=True)
    salary_max = models.PositiveIntegerField( null=True, blank=True)
    remote = models.BooleanField(default=False)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES)
    is_public = models.BooleanField(default=True)
    external_apply_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    required_skills = models.TextField(help_text="Enter skills in point form", blank=True)
    education_experience = models.TextField(help_text="Enter educational and experience requirements", blank=True)
    application_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class Application(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='applications'
    )
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications'
    )
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='applied')  # e.g., 'shortlisted', 'rejected'

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"


