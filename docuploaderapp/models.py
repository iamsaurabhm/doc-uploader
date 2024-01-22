from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Paraplanner(models.Model):
    paraplanner = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.paraplanner


class Status(models.Model):
    status = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "status"

    def __str__(self):
        return self.status
 

class Document(models.Model):
    company_name = models.CharField(max_length=100, default='')
    client_name = models.CharField(max_length=100, default='')
    adviser_name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    submitted_at = models.DateField(auto_now_add=False, editable=True, null=True, blank=False)
    due_date = models.DateField(null=True, blank=False)
    paraplanner = models.ForeignKey(Paraplanner, null=True, on_delete=models.SET_NULL,)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL, blank=True)
    document = models.FileField(upload_to='documents', blank=True)
    query = models.TextField(max_length=500)

    class Meta:
        ordering = ('-created_at',)
