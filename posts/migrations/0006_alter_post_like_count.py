# Generated by Django 4.0.6 on 2022-07-29 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_like_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Like'),
        ),
    ]
