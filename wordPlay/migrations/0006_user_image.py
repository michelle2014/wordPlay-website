# Generated by Django 3.0.8 on 2020-11-03 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordPlay', '0005_auto_20201102_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
