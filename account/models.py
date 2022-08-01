from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from post.models.author_models import Profile
# create your models here

# def user_pre_save(sender, instance, *args, **kwargs):
#     if instance:
#         Profile.objects.create(user=instance)

# pre_save.connect(user_pre_save, sender=settings.AUTH_USER_MODEL)
