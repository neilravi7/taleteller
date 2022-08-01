from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from random import randint

from taggit.managers import TaggableManager

from post.utils import count_words, read_time
from post.models.category_models import Category


class Article(models.Model):

    # Article status constants
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"

    # CHOICES
    STATUS_CHOICES = (
        (DRAFTED, 'Draft'),
        (PUBLISHED, 'Publish'),
    )

    # BLOG MODEL FIELDS
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.CharField(max_length=150, blank=True, null=True)
    image_credit = models.CharField(max_length=150, null=True, blank=True)
    body = models.TextField()
    tags = TaggableManager(blank=True)
    date_published = models.DateTimeField(null=True, blank=True,
                                          default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='DRAFT')
    views = models.PositiveIntegerField(default=0)
    count_words = models.CharField(max_length=50, default=0)
    read_time = models.CharField(max_length=50, default=0)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("title",)
        ordering = ('-date_published',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.image = f"https://picsum.photos/id/{randint(1,1025)}/280/100"
        self.count_words = count_words(self.body)
        self.read_time = read_time(self.body)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post:article_detail', kwargs={'slug': self.slug})


