# Generated by Django 3.1.5 on 2021-01-21 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(to='auctions.Listing'),
        ),
    ]
