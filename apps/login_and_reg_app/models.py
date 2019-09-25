from django.db import models
import datetime
import bcrypt
import re

class UserDataManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # First Name
        if len(postData['first_name']) < 2:
            errors["First Name"] = "First  name should be at least 2 characters"
        if not re.match(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",postData['first_name']):
            errors["Invalid First Name"] = "Invalid first name"
        
        # Last Name
        if len(postData['last_name']) < 2:
            errors["Last Name"] = "Last name should be at least 2 characters"
        if not re.match(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",postData['last_name']):
            errors["Invalid Last Name"] = "Invalid last name"
        
        #email
        if len(postData['email'])<5:
            errors["email"] = "Email should be at least 5 characters and with a valid format. i.e.: something@domain.com"
        
        #password
        if len(postData['password'])<8 or len(postData['password'])>254:
            errors["Password length"] = "Password size must be between 8 and 254 characters "
        
        commom_passwords = ['Password1', 'password123']
        for x in range(len(commom_passwords)):
            if postData['password'] == commom_passwords[x]:
                errors["Common password"] = "The password is very common and unsafe"

        # #birthday date
        # #---- COMMENTING BECAUSE IT NEEDS TO BE IMPLEMENTED IN THE TEMPLATE-------
        # if str(postData['birthday']) == "":
        #     errors["birthday"] = "Release date should not be empty."
        # else: 
        #     now = datetime.datetime.utcnow()
        #     if datetime.datetime.strptime(str(postData['birthday']), '%Y-%m-%d') > now - datetime.timedelta(days=18*365):
        #         errors["birthday date"] = "birthdate must be priot be in the future."

        #password
        if postData['password'] != postData['conf_password']:
            errors["Unmatching passwords"] = "Passwords don't match"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserDataManager()
    
