from django.db import models
from phone_field import PhoneField
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import datetime

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
    box_id = models.IntegerField(unique=True)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_shelf = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.box_id)
    class Meta:
        # ordering = ["box_id"]
        verbose_name_plural = "boxes"


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
        return str(self.name)

    def get_subjects_at_same_location(self):
        subjects = Subject.objects.filter(location=self.location)
        return subjects
    
    @property
    def is_complete(self):
        """
        Check if current date is after collection date
        """
        if self.date < datetime.now().date():
            return True
        else:
            return False




class Sample(models.Model):
    COLLECTION_CHOICES = [
    ('COLLECTED', 'Collected'),
    ('NOT_COLLECTED', 'Not Collected'),
    ('PENDING', 'Pending')
    ]
    sample_id = models.CharField(max_length=6, unique=False)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    box = models.ForeignKey(Box, on_delete=models.PROTECT, null=True, blank=True)
    box_position = models.IntegerField(null=True, blank=True)
    collection_event = models.ForeignKey(Event, on_delete=models.PROTECT)
    collection_status = models.CharField(max_length=15, choices=COLLECTION_CHOICES, default='PENDING')
    
    def __str__(self):
        return str(self.sample_id)

    def get_samples_for_event(event):
        samples = Sample.objects.filter(collection_event=event)
        return samples

    def get_subjects_at_event(event):
        """
        Returns a dictionary of subjects assigned to the same
        location as event. If a subject already has an associated
        sample for this event it will be listed under the 'created'
        key, otherwise it will be listed under the 'not_created' key.
        """
        subjects = event.get_subjects_at_same_location()
        subjects_dict = {'created': [], 'not_created': []}
        for subject in subjects:
            # Check if a sample has already been made for this event with this subject
            sample = Sample.objects.filter(collection_event=event).filter(subject=subject)
            if len(sample):
                subjects_dict['created'].append(subject)
            else:
                subjects_dict['not_created'].append(subject)
        return subjects_dict




