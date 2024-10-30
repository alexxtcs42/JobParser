from django.db import models


class Vacancy(models.Model):
    vacancy_id = models.IntegerField(null=False)
    url = models.URLField()
    vacancy_title = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    salary_from = models.IntegerField()
    salary_to = models.IntegerField()
    salary_currency = models.CharField(max_length=100)
    is_archived = models.BooleanField()
    working_days = models.BooleanField(default=False)
    time_intervals = models.BooleanField(default=False)
    time_modes = models.BooleanField(default=False)
    experience = models.CharField(max_length=100)
    employment = models.CharField(max_length=100)

    def __str__(self):
        return self.vacancy_id

    class Meta:
        verbose_name_plural = "Vacancies"
