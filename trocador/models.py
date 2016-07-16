from django.db import models
from django.utils import timezone

class Trocador(models.Model):
    author = models.ForeignKey('auth.User')
    fluido1 = models.CharField(max_length=500)
    fluido2 = models.CharField(max_length=500)
    material = models.CharField(max_length=500)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title