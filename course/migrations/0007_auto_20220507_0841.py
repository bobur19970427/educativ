# Generated by Django 3.2.12 on 2022-05-07 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_lesson_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledge',
            name='course',
        ),
        migrations.AddField(
            model_name='knowledge',
            name='course',
            field=models.ManyToManyField(related_name='knowledges', to='course.Course'),
        ),
        migrations.RemoveField(
            model_name='whom',
            name='course',
        ),
        migrations.AddField(
            model_name='whom',
            name='course',
            field=models.ManyToManyField(related_name='whoms', to='course.Course'),
        ),
    ]
