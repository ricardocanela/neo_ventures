from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    bio = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.company_name

class Demand(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Solution(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    demands = models.ManyToManyField(Demand, related_name='solutions', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title