# Generated by Django 2.2.2 on 2019-07-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_category_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
