# Generated by Django 3.0.3 on 2020-03-03 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0003_auto_20200303_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='current_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Room'),
        ),
    ]
