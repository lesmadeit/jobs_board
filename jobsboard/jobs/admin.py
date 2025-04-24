from django.contrib import admin

from .models import CompanyProfile, Job, Application, Testimonial, BlogCategory, BlogPost, BlogReply, BlogLike

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author__username')

admin.site.register(CompanyProfile)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Testimonial)
admin.site.register(BlogCategory)
admin.site.register(BlogReply)
admin.site.register(BlogLike)
