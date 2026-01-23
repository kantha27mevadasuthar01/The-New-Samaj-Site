from django.db import models

class SamajInformation(models.Model):
    SECTION_CHOICES = [
        ('HISTORY', 'History'),
        ('PURPOSE', 'Purpose/Goal'),
        ('VALUES', 'Values'),
    ]
    
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_section_display()
    
    class Meta:
        verbose_name_plural = "Samaj Information"
