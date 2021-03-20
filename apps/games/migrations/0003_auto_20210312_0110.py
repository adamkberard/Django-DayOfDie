# Generated by Django 3.1.4 on 2021-03-12 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20210310_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='typeOfPoint',
            field=models.CharField(choices=[('PT', 'regular point'), ('SS', 'self sink'), ('TK', 'tink'), ('SK', 'sink'), ('BS', 'bounce sink'), ('PS', 'partner sink')], default='PT', max_length=2),
        ),
    ]
