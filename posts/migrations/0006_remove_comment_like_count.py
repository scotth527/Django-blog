# Generated by Django 3.1.6 on 2021-03-02 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='like_count',
        ),
    ]
