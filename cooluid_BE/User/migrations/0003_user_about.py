# Generated by Django 4.2.6 on 2023-10-30 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_registrationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
