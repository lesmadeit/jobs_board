from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
path('dashboard/summary/', views.dashboard_summary, name="dashboard_summary"),
path('dashboard/jobs/', views.job_listings_management, name="job_listings_management"),
path('job/<int:pk>/edit/', views.edit_job, name='edit_job'),
path('job/<int:pk>/close/', views.close_job, name='close_job'),
path('job/<int:pk>/delete/', views.delete_job, name='delete_job'),
path('dashboard/job/<int:pk>/applicants/', views.applicants_management, name='applicants_management'),
path('application/<int:application_id>/status/<str:status>/', views.update_application_status, name='update_application_status'),
path('application/<int:application_id>/resume/', views.download_resume, name='download_resume'),

]