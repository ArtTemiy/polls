# Generated by Django 3.0.5 on 2021-01-24 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.Answer'),
        ),
    ]