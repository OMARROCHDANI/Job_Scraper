# Generated by Django 4.2.2 on 2023-10-26 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_savedjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedjob',
            name='payment',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
