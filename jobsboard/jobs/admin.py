from django.contrib import admin

from .models import CompanyProfile, Job, Application

admin.site.register(CompanyProfile)
admin.site.register(Job)
admin.site.register(Application)
