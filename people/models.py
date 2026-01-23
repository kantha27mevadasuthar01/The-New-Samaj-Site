from django.db import models

class FamilyGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Family Name/Identity")
    village = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.village})"

class Person(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    age = models.PositiveIntegerField()
    native_gam = models.CharField(max_length=100, verbose_name="Native Village (Gam)")
    current_city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='people_photos/', blank=True, null=True)
    
    family_group = models.ForeignKey(FamilyGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    is_family_head = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.age})"
    
    class Meta:
        verbose_name_plural = "People Directory"
        ordering = ['-is_family_head', 'full_name']
