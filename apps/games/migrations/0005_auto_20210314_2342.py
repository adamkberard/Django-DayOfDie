# Generated by Django 3.1.4 on 2021-03-14 23:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0004_game_timestarted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='scoredOn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scored', to=settings.AUTH_USER_MODEL),
        ),
    ]