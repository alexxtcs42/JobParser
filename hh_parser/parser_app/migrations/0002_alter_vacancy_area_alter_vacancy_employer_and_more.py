# Generated by Django 4.2.16 on 2024-10-30 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='area',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='employer',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='employment',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='experience',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_currency',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='vacancy_title',
            field=models.CharField(max_length=100),
        ),
    ]
