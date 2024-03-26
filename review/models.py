from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_user_user")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_manager_user")
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_reviewer_user")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee_employee")
    rate = models.IntegerField(default=5)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"

class Feedback(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_feedback")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee_feedback")
    rate = models.IntegerField(default=5)
    text = models.TextField()
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"

