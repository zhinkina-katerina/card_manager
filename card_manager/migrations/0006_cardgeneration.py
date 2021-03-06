# Generated by Django 3.2.14 on 2022-07-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_manager', '0005_transaction_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardGeneration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('New', 'New'), ('In_process', 'In Process'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='New', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=0)),
                ('exception', models.TextField(default='')),
            ],
        ),
    ]
