from django.db import models

class Family(models.Model):
    """
    Represents a family unit in the community.
    Grouped by hometown, with one person designated as the head of the family.
    """
    hometown = models.CharField(max_length=100, verbose_name="Home Town")
    head = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_family')
    
    def __str__(self):
        head_name = self.head.full_name if self.head else "No Head"
        return f"{head_name}'s Family ({self.hometown})"

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['hometown']

class Person(models.Model):
    """
    Represents an individual member of the community.
    Stores personal details, family relations, educational and professional info.
    """
    RELATION_CHOICES = [
        ('HEAD', 'Head of Family'),
        ('SPOUSE', 'Spouse'),
        ('SON', 'Son'),
        ('DAUGHTER', 'Daughter'),
        ('GRANDSON', 'Grandson'),
        ('GRANDDAUGHTER', 'Granddaughter'),
        ('OTHER', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('MARRIED', 'Married'),
        ('UNMARRIED', 'Unmarried'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    EDUCATION_CHOICES = [
        ('SSC', 'SSC'),
        ('HSC', 'HSC'),
        ('DIPLOMA', 'Diploma'),
        ('GRADUATE', 'Graduate'),
        ('POST_GRADUATE', 'Post Graduate'),
        ('DOCTORATE', 'Doctorate'),
        ('CA', 'CA'),
        ('CS', 'CS'),
        ('LLB', 'LLB'),
        ('MBBS', 'MBBS'),
        ('OTHER', 'Other'),
    ]

    # Personal Information
    photo = models.ImageField(upload_to='people_photos/', blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    relation_with_head = models.CharField(max_length=20, choices=RELATION_CHOICES, default='OTHER')
    is_head = models.BooleanField(default=False, verbose_name="Is Head of Family")
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='UNMARRIED')
    
    birth_date = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES, blank=True)
    education_other = models.CharField(max_length=200, blank=True, null=True, verbose_name="Other Education")
    
    maternal_home = models.CharField(max_length=200, blank=True, null=True, verbose_name="Maternal Home")
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    address = models.TextField(blank=True)
    job = models.CharField(max_length=200, blank=True, verbose_name="Job/Profession")
    mobile_number = models.CharField(max_length=15, blank=True)
    
    # Family Linkage
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members', null=True, blank=True)
    
    # For grandchildren logic: link a person to their parent who is a child in this family
    parent_person = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_people')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "People Directory"
        ordering = ['family__hometown', 'full_name']
