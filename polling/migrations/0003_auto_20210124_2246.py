# Generated by Django 3.0.5 on 2021-01-24 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0002_auto_20210124_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='text',
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
    ]