# Generated by Django 5.1.2 on 2024-11-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodapp', '0007_alter_confirmbuydetails_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmbuydetails',
            name='total_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
