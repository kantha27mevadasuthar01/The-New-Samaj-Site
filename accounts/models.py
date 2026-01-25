from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.validators import UnicodeUsernameValidator

class SpaceUnicodeUsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w. \-+]+$'

class User(AbstractUser):
    username_validator = SpaceUnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_/space only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SUB_ADMIN = 'SUB_ADMIN', 'Sub-Admin'
        MEMBER = 'MEMBER', 'Member'
        PUBLIC = 'PUBLIC', 'Public'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PUBLIC
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    can_view_directory = models.BooleanField(default=False, verbose_name="Can view People Directory")
    
    def is_samaj_admin(self):
        return self.role in [self.Role.ADMIN, self.Role.SUB_ADMIN] or self.is_superuser

    def is_main_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_samaj_member(self):
        return self.role in [self.Role.MEMBER, self.Role.ADMIN, self.Role.SUB_ADMIN]

class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=255)
    target = models.CharField(max_length=255, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.actor} - {self.action} - {self.timestamp}"
