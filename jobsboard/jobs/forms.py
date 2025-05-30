from django import forms
from .models import *
from .models import CompanyProfile, Job, Application, Testimonial, Message, ResponseTemplate







class ContactusForm(forms.Form):
    Name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control valid',
            'id': 'name',
            'placeholder': 'Enter your name',
            'onfocus': "this.placeholder = ''",
            'onblur': "this.placeholder = 'Enter your name'"
        })
    )
    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control valid',
            'id': 'email',
            'placeholder': 'Enter email address',
            'onfocus': "this.placeholder = ''",
            'onblur': "this.placeholder = 'Enter email address'"
        })
    )
    Subject = forms.CharField(
    max_length=100,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'subject',
        'placeholder': 'Enter Subject',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Enter Subject'"
    })
    )
    Message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control w-100',
            'id': 'message',
            'rows': 9,
            'cols': 30,
            'placeholder': 'Enter Message',
            'onfocus': "this.placeholder = ''",
            'onblur': "this.placeholder = 'Enter Message'"
        })
    )


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'industry', 'description', 'website', 'email', 'logo', 'location']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter company email'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'industry', 'location', 'job_type',
            'salary_min', 'salary_max', 'remote', 'experience_level',
            'is_public', 'external_apply_url', 'featured', 'required_skills', 'education_experience',
            'application_deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'industry': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'remote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'external_apply_url': forms.URLInput(attrs={'class': 'form-control'}),
            'required_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List skills in point form'}),
            'education_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List education and experience requirements in point form'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }





class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter', 'portfolio_url']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your cover letter here...'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourportfolio.com'}),
        }



class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'title', 'message', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your testimonial here'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body', 'job']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
            'job': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if company:
            self.fields['job'].queryset = company.jobs.all()
            self.fields['job'].empty_label = 'General Inquiry (No Job Selected)'

class ResponseTemplateForm(forms.ModelForm):
    class Meta:
        model = ResponseTemplate
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Template Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Template Content', 'rows': 4}),
        }
