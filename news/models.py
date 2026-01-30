from django.db import models

class NewsAnnouncement(models.Model):
    message = models.TextField(help_text="The announcement text to display in the scroller.")
    is_active = models.BooleanField(default=True, help_text="Toggle visibility of this announcement.")
    scroll_speed = models.IntegerField(default=20, help_text="Speed in seconds (e.g., 20 = Slow, 10 = Fast).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message[:50]}..."
