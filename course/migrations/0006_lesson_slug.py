# Generated by Django 3.2.12 on 2022-05-07 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_lesson_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]