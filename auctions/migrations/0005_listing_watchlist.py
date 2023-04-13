# Generated by Django 4.1.3 on 2022-12-05 21:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='listingwatchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]