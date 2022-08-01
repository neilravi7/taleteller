from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from random import randint


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors_profile')
    image = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(
        max_length=100, blank=True, null=True, help_text="short Bio (eg: i love cats and games)")
    address = models.CharField(max_length=100, blank=True, null=True, help_text="Enter your address")
    city = models.CharField(max_length=20, blank=True, null=True, help_text="Enter your city")
    state = models.CharField(max_length=20, blank=True, null=True, help_text="Enter your state")
    country = models.CharField(max_length=20, help_text="Enter your country", blank=True, null=True)
    zip_code = models.CharField(max_length=20, help_text="Enter your zipcode", blank=True, null=True)
    twitter_url = models.CharField(max_length=150, default="#", blank=True,
                                   null=True, help_text="Enter # if you don't have an account")
    facebook_url = models.CharField(max_length=150, default="#", blank=True,
                                    null=True, help_text="Enter # if you don't have an account")
    instagram_url = models.CharField(
        max_length=150, default="#", blank=True, null=True, help_text="Enter # if you don't have an account")
    email_confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        # get randomize hosted images from url (user profile pictures)
        self.image = "http://placebeard.it/640/480/notag" # f"https://picsum.photos/id/{randint(0, 1100)}/200/300"
        super(Profile, self).save(*args, **kwargs)