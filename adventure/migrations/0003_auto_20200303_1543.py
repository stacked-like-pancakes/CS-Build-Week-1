# Generated by Django 3.0.3 on 2020-03-03 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200303_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='current_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Room'),
        ),
    ]