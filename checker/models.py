from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symptoms = models.ManyToManyField(Symptom, related_name='diseases')
    description = models.TextField(blank=True)
    info_link = models.URLField(blank=True, help_text="Link to learn more about this disease")

    def __str__(self):
        return self.name
