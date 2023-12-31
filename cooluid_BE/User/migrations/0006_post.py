# Generated by Django 4.2.6 on 2023-10-31 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('isPublic', models.BooleanField(default=False)),
                ('movie_title', models.CharField(max_length=255)),
                ('movie_director', models.CharField(max_length=255)),
                ('posterurl', models.URLField()),
                ('movieId', models.CharField(max_length=20)),
            ],
        ),
    ]
