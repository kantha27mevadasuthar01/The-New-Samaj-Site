from django.db import models

class MandirLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField(blank=True, help_text="About the temple/location")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    google_maps_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"
