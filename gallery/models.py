from django.db import models

class MediaItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
    ]
    
    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='samaj_media/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="For YouTube links")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
        
    def get_embed_url(self):
        if self.video_url and "youtube.com" in self.video_url:
            # Simple replace for demo purposes
            return self.video_url.replace("watch?v=", "embed/")
        if self.video_url and "youtu.be" in self.video_url:
             return self.video_url.replace("youtu.be/", "www.youtube.com/embed/")
        return self.video_url
