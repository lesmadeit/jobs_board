from django import forms
from .models import *



class JobSearchForm(forms.Form):
    keyword = forms.CharField(max_length=255, required=False, label="Keyword")
    job_type = forms.ChoiceField(choices=[('', 'Any')] + Job.JOB_TYPES, required=False, label="Job Type")
    location = forms.CharField(max_length=255, required=False)
    industry = forms.CharField(max_length=255, required=False)
    experience_level = forms.ChoiceField(choices=[('', 'Any')] + Job.EXPERIENCE_LEVELS, required=False)
    min_salary = forms.DecimalField(required=False, label="Minimum Salary")
    max_salary = forms.DecimalField(required=False, label="Maximum Salary")
