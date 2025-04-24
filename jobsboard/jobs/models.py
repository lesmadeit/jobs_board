from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils import timezone


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

POSTED_WITHIN_CHOICES = (
    ('any', 'Any'),
    ('1', 'Today'),
    ('2', 'Last 2 days'),
    ('3', 'Last 3 days'),
    ('5', 'Last 5 days'),
    ('10', 'Last 10 days'),
)

INDUSTRY_CHOICES = (
    ('tech', 'Technology'),
    ('engineering', 'Engineering'),
    ('medicine', 'Medicine'),
    ('construction', 'Construction'),
    ('manufacturing', 'Manufacturing'),
    ('law', 'Law'),
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
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    salary_min = models.PositiveIntegerField( null=True, blank=True)
    salary_max = models.PositiveIntegerField( null=True, blank=True)
    remote = models.BooleanField(default=False)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES)
    is_public = models.BooleanField(default=True)
    external_apply_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    required_skills = models.TextField(help_text="Enter skills in point form", blank=True)
    education_experience = models.TextField(help_text="Enter educational and experience requirements", blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

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
    status = models.CharField(max_length=50,
                              choices=[
                                  ('applied', 'Applied'),
                                  ('shortlisted', 'Shortlisted'),
                                  ('rejected', 'Rejected'),
                                  ('hired', 'Hired'),
                              ],
                              default='applied')

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
    

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE, related_name='testimonials', null=True, blank=True)

    def __str__(self):
        return self.name
    

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class BlogReply(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class Meta:
        verbose_name_plural = "Replies"

    def __str__(self):
        return f"Reply by {self.author.username} on {self.blog_post.title}"
    
    def get_replies(self):
        return self.children.all().order_by('created_at')
    


class BlogLike(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog_post', 'user')  # Prevents duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.blog_post.title}"
    



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient_company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE, related_name='received_messages')
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} to {self.recipient_company}: {self.subject}"
    

class ResponseTemplate(models.Model):
    company = models.ForeignKey('CompanyProfile', on_delete=models.CASCADE, related_name='response_templates')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.company})"


