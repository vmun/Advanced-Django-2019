# Generated by Django 2.2.2 on 2019-07-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_category_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='tilt',
            field=models.CharField(default='e', max_length=200),
            preserve_default=False,
        ),
    ]
