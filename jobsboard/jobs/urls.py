from django.urls import path
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("service-details/", views.service_details, name="service-details"),
    path("blog/", views.blog, name="blog"),
    path("blog-details/", views.blog_details, name="blog-details"),
    path("contact/", views.contact, name="contact"),
    path("jobs/", views.job_list, name="jobs"),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/edit/', views.job_update, name='job_update'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:pk>/applicants/', views.view_applicants, name='view_applicants'),
    path('company/create/', views.company_profile_create, name='company_profile_create'),
    path('company/edit/', views.company_profile_update, name='company_profile_update'),
    path('company/profile/', views.company_profile_view, name='company_profile_view'),

]