from django.db import models
from customer.models import Customer

# Create your models here.
class CourseType(models.Model):
    name = models.CharField()
    description = models.TextField()

class Course(models.Model):
    name = models.CharField()
    type = models.OneToOneField(CourseType, on_delete=models.CASCADE, related_name='type')
    customers = models.ManyToManyField(Customer, blank=True)
    availability = models.IntegerField(default=10)