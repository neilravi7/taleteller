# Generated by Django 4.0.5 on 2022-07-15 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('job_title', models.CharField(max_length=50)),
                ('bio', models.CharField(help_text='short Bio (eg: i love cats and games)', max_length=100)),
                ('address', models.CharField(help_text='Enter your address', max_length=100)),
                ('city', models.CharField(help_text='Enter your city', max_length=20)),
                ('state', models.CharField(help_text='Enter your state', max_length=20)),
                ('country', models.CharField(help_text='Enter your country', max_length=20)),
                ('zip_code', models.CharField(help_text='Enter your zipcode', max_length=20)),
                ('twitter_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=150, null=True)),
                ('facebook_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=150, null=True)),
                ('instagram_url', models.CharField(blank=True, default='#', help_text="Enter # if you don't have an account", max_length=150, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authors_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
