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

class Feedback(models.Model):
    rating = models.IntegerField()
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating}"


    def __str__(self):
        return self.name
