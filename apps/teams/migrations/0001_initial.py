# Generated by Django 3.2.7 on 2021-09-24 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('bl', 'Blocked'), ('pd', 'Pending'), ('ac', 'Accepted'), ('nt', 'Nothing')], default='pd', max_length=2)),
                ('team_captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_captain', to=settings.AUTH_USER_MODEL)),
                ('teammate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teammate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
