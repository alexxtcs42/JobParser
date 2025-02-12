# Generated by Django 4.2.16 on 2024-10-30 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_id', models.IntegerField()),
                ('url', models.URLField()),
                ('vacancy_title', models.TextField()),
                ('employer', models.TextField()),
                ('area', models.TextField()),
                ('salary_from', models.IntegerField()),
                ('salary_to', models.IntegerField()),
                ('salary_currency', models.TextField()),
                ('is_archived', models.BooleanField()),
                ('working_days', models.BooleanField(default=False)),
                ('time_intervals', models.BooleanField(default=False)),
                ('time_modes', models.BooleanField(default=False)),
                ('experience', models.TextField()),
                ('employment', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Vacancies',
            },
        ),
    ]
