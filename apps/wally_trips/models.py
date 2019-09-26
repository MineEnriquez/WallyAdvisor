from django.db import models
from ..login_and_reg_app.models import User
import datetime
import bcrypt
import re



class TripDataManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # Destination
        if len(postData['destination']) < 3:
            errors["Destination"] = "A trip destination must consist of at least 3 characters"

        if len(postData['plan']) < 3:
            errors["Plan"] = "A plan must be provided!"
        if str(postData['start_date']) == "":
            errors["Start date"] = "Start date should not be empty."
        if str(postData['end_date']) == "":
            errors["End date"] = "End date should not be empty."
        return errors

# class Trips(models.Model):
#     destination = models.CharField(max_length=50)
#     zipcode = models.CharField(max_length=50)
#     # user = models.ForeingKey(User)
#     created_at = models.DateTimeField(auto_now=True)
#     updated_at = models.DateTimeField(auto_now=True)


class Trips(models.Model):
    destination = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=12)
    start_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name="user")
    objects = TripDataManager()