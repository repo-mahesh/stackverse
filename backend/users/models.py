from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class PremiumUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=100, blank=True)
    # Existing field
    is_premium = models.BooleanField(default=False)
    
    # Additional useful fields
    premium_start_date = models.DateTimeField(null=True, blank=True)
    premium_end_date = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.URLField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email or self.username

    @property
    def is_premium_active(self):
        if not self.is_premium:
            return False
        if not self.premium_end_date:
            return False
        return timezone.now() <= self.premium_end_date

    def activate_premium(self, duration_days=30):
        self.is_premium = True
        self.premium_start_date = timezone.now()
        self.premium_end_date = timezone.now() + timezone.timedelta(days=duration_days)
        self.save()

