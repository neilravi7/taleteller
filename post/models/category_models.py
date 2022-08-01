from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from random import randint

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField()
    # will be uncommented after taking Amazon S3 - Cloud Object Storage.
    # image = models.ImageField(default="xyz.jpg", upload_to="category_images")
    image = models.CharField(max_length=200)
    approved = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = slugify(self.name, allow_unicode=True)
        self.image = f"https://picsum.photos/id/{randint(1,1025)}/300"
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'post:category_post',
            kwargs={
                "slug": self.slug
            }
        )
