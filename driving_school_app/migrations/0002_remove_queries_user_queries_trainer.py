# Generated by Django 4.1 on 2024-04-11 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('driving_school_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='queries',
            name='user',
        ),
        migrations.AddField(
            model_name='queries',
            name='trainer',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='driving_school_app.trainer'),
        ),
    ]
