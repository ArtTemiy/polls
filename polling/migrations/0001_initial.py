# Generated by Django 3.0.5 on 2021-01-19 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=1024)),
                ('text', models.CharField(default=None, max_length=1024)),
                ('answer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polling.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024)),
                ('ttype', models.CharField(choices=[('T', 'Text'), ('O', 'One answer'), ('S', 'Several answers')], max_length=1)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.Poll')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling.Question'),
        ),
    ]
