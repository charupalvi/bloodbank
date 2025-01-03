# Generated by Django 5.1.2 on 2024-11-08 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slider_images/')),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
