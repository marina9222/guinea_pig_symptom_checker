from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    info_link = models.URLField(blank=True, null=True)
    symptoms = models.ManyToManyField('Symptom', related_name='diseases')

    


    def __str__(self):
        return self.name
