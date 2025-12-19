from django.db import models
from django.contrib.auth.models import User

POST_TYPES = (
    ('photo', 'Photo'),
    ('video', 'Video'),
    ('text', 'Text'),
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    location = models.CharField(max_length=200)
    education = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.message
