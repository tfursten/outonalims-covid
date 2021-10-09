from django.db import models
from phone_field import PhoneField
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    investigator = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True) 
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.name)

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = PhoneField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Subject(models.Model):

    SEX_CHOICES = [
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ]
    VACCINE_CHOICES = [
        ('FULL', 'Full'),
        ('PARTIAL', 'Partial'),
        ('NO', 'None')
    ]
    COVID_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    subject_ui = models.CharField(max_length=6, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    vaccine_status = models.CharField(max_length=10, choices=VACCINE_CHOICES, blank=True, null=True)
    covid = models.CharField(max_length=10, choices=COVID_CHOICES, null=True, blank=True, help_text="Has subject been infected with COVID-19 prior to study")
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.subject_ui

class Box(models.Model):
    box_id = models.IntegerField()
    storage_location = models.CharField(max_length=100)
    storage_shelf = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.box_id)





class Sample(models.Model):
    sample_id = models.CharField(max_length=6, primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.PROTECT)
    box = models.ForeignKey(Box, on_delete=models.PROTECT)
    box_location = models.IntegerField()
    project = models.CharField(max_length=100)
    collection_event = models.CharField(max_length=100)
    collected = models.BooleanField()
    
    def __str__(self):
        return self.sample_id




class Researcher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    researcher = models.ForeignKey(Researcher, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.location, self.date





