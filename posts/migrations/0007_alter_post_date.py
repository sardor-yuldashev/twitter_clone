# Generated by Django 4.0.6 on 2022-07-29 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_post_like_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date'),
        ),
    ]
