# Generated by Django 3.2.12 on 2022-05-07 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20220507_0841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('order', models.IntegerField(default=0)),
                ('course', models.ManyToManyField(related_name='requiremnts', to='course.Course')),
            ],
        ),
    ]