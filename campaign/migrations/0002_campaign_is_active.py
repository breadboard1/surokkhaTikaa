# Generated by Django 5.1.2 on 2024-11-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
