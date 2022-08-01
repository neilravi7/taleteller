from django.test import TestCase
from .models import Category
from faker import Faker

fake = Faker()
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        # Creating Category
        for i in range(2):
            Category.objects.create(name=fake.username())