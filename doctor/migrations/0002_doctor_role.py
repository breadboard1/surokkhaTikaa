# Generated by Django 5.1.2 on 2024-11-05 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='role',
            field=models.CharField(default='Doctor', editable=False, max_length=10),
        ),
    ]
