from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
import datetime


class Contact(models.Model):
    first_name = models.CharField(validators=[MinLengthValidator(3)], max_length=20)
    last_name = models.CharField(validators=[MinLengthValidator(3)], max_length=20)
    phone_number = models.CharField(validators=[MinLengthValidator(13)], max_length=13)


class Message(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    delivered_datetime = models.DateTimeField(default=datetime.datetime.now())
    message = models.TextField(validators=[MinLengthValidator(5), MaxLengthValidator(100)])
