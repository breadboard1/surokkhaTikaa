# Generated by Django 5.1.2 on 2024-11-05 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_campaign_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignreview',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='campaign.campaign'),
        ),
    ]