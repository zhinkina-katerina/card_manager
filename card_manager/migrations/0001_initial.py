# Generated by Django 3.2.14 on 2022-07-13 08:26

import card_manager.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BIN', models.CharField(max_length=6, validators=[card_manager.models.check_for_invalid_characters])),
                ('number', models.CharField(max_length=8, validators=[card_manager.models.check_for_invalid_characters])),
                ('issue_date', models.DateTimeField()),
                ('expired', models.DateTimeField()),
                ('cvv', models.CharField(max_length=3, validators=[card_manager.models.check_for_invalid_characters])),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('activated', 'Activated'), ('not_activated', 'Not activated'), ('expired', 'Expired')], default='not_activated', max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('amount', models.IntegerField(max_length=10)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card_manager.card')),
            ],
        ),
    ]
