# Generated by Django 3.0.8 on 2020-12-01 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wordPlay', '0015_auto_20201130_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='wordPlay.Word'),
        ),
    ]
