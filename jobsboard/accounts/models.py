from django.db import models
from django.contrib.auth.models import User
from PIL import Image

ROLE_CHOICES = (
    ('candidate', 'Candidate'),
    ('employer', 'Employer'),
)

# Extending User Model Using a One-To-One link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    def __str__(self):
        return self.user.username
    

    # resizing image
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

