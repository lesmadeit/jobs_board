from django.db import models

class Job(models.Model):
    JOB_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
    ]

    EXPERIENCE_LEVELS = [
        ('Entry', 'Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior Level'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVELS)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    descriprion = models.TextField()

    def __str__(self):
        return self.title
