# Generated by Django 3.2.14 on 2022-07-14 17:09

import card_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_manager', '0007_cardgeneration_activity_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardgeneration',
            name='BIN',
            field=models.CharField(default=0, max_length=6, validators=[card_manager.models.check_for_invalid_characters]),
            preserve_default=False,
        ),
    ]
