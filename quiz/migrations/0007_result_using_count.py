# Generated by Django 3.2.6 on 2024-02-12 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20240211_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='using_count',
            field=models.IntegerField(default=0),
        ),
    ]
