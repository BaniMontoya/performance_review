from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_user")
    creation_date = models.DateTimeField(default=timezone.now)

class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_owner")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    rate = models.IntegerField(default=5)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)

class Feedback(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_feedback")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_feedback")
    rate = models.IntegerField(default=5)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)