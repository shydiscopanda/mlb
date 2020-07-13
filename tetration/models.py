from django.db import models


# Create your models here.
class Result(models.Model):
    incoming_val = models.IntegerField(primary_key=True)
    calculated_val = models.TextField()


class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    job_id = models.CharField(max_length=128)
    result = models.CharField(max_length=128, blank=True, null=True)
