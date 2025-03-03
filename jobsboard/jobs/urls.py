from django.urls import path
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("service-details/", views.service_details, name="service-details"),
    
    path("contact/", views.contact, name="contact"),
    path("jobs/", views.job_list, name="jobs"),
    path('featured-jobs/', views.featured_jobs, name='featured_jobs'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/create/', views.job_create, name='job_create'),
    path('job/<int:pk>/edit/', views.job_update, name='job_update'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:pk>/applicants/', views.view_applicants, name='view_applicants'),
    path('company/create/', views.company_profile_create, name='company_profile_create'),
    path('company/edit/', views.company_profile_update, name='company_profile_update'),
    path('company/profile/', views.company_profile_view, name='company_profile_view'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('edit-testimonial/<int:pk>/', views.edit_testimonial, name='edit_testimonial'),
    path('delete-testimonial/<int:pk>/', views.delete_testimonial, name='delete_testimonial'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/reply/<int:blog_id>/', views.add_reply, name='add_reply'),
    path('blog/reply/<int:blog_id>/<int:parent_id>/', views.add_reply, name='add_reply'),
    path('blog/delete-reply/<int:blog_id>/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('blog/like/<int:blog_id>/', views.toggle_like, name='toggle_like'),

]