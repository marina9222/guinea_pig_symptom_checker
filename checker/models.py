from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symptoms = models.ManyToManyField(Symptom)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name