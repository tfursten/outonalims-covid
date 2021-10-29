from django.db import models
from phone_field import PhoneField
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import datetime
from cualid import create_ids
from django.contrib.auth.models import User

# 
# Create your models here.

User._meta.get_field('email').blank = False

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
    classroom = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = PhoneField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ('name', )

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
    GRADE_CHOICES = [
        ('K', 'K'),
        ('NH', 'NH')
    ]
    GRADE_CHOICES += [(str(i), str(i)) for i in range(1, 13)]
    subject_ui = models.CharField(max_length=6, blank=True, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    race = models.CharField(max_length=100, null=True, blank=True)
    ethnicity = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    phone = PhoneField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    gardian_name = models.CharField(max_length=100, null=True, blank=True)
    gardian_relationship = models.CharField(max_length=100, null=True, blank=True)
    teacher_name = models.CharField(max_length=100, null=True, blank=True)
    vaccine_status = models.CharField(max_length=10, choices=VACCINE_CHOICES, blank=True, null=True)
    dose_1 = models.DateField(null=True, blank=True)
    dose_2 = models.DateField(null=True, blank=True)
    dose_3 = models.DateField(null=True, blank=True)
    prior_covid = models.CharField(
        max_length=10, choices=COVID_CHOICES, null=True, blank=True,
        help_text="Has subject been infected with COVID-19 prior to study")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.subject_ui: # only if subject_ui is blank
            existing_ids = [subj.subject_ui for subj in Subject.objects.all() if subj.subject_ui]
            cualid = create_ids(1, 6, existing_ids=existing_ids)
            self.subject_ui = [cid[0] for cid in create_ids(1, 6, existing_ids=existing_ids)][0]
            self.save()

    def __str__(self):
        return self.subject_ui

class Box(models.Model):
    box_name = models.CharField(max_length=100, unique=True)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_shelf = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.box_name)
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
    location = models.ManyToManyField(Location)
    researcher = models.ForeignKey(Researcher, on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.name)

    def get_subjects_at_same_location(self):
        locations = self.location.all()
        subjects = []
        subjects = Subject.objects.filter(location__in=locations)
        print(subjects)
        # for location in locations:
        #     print(location)
        #     print(Subject.objects.filter(location=location))
        #     subjects.append(Subject.objects.filter(location=location))[:]
        # print(subjects)
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
    ('Collected', 'Collected'),
    ('Not Collected', 'Not Collected'),
    ('Pending', 'Pending')
    ]
    name = models.CharField(max_length=6, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    box = models.ForeignKey(Box, on_delete=models.PROTECT, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)
    box_position = models.IntegerField(null=True, blank=True)
    collection_event = models.ForeignKey(Event, on_delete=models.PROTECT)
    collection_status = models.CharField(max_length=15, choices=COLLECTION_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return str(self.name)

    def get_samples_for_event(event, sort_by1="NAME", sort_by2="GRADE", sort_by3="LOCATION"):
        sortby = {
            'GRADE': 'subject__grade',
            'NAME': 'subject__last_name',
            'LOCATION': 'subject__location'
            }
        samples = Sample.objects.filter(collection_event=event).order_by(
            sortby[sort_by1], sortby[sort_by2], sortby[sort_by3])
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



class Pool(models.Model):
    STATUS_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Pending', 'Pending')
    ]
    name = models.CharField(max_length=100, unique=True)
    samples = models.ManyToManyField(Sample, blank=True)
    pools = models.ManyToManyField('Pool', symmetrical=False, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    box = models.ForeignKey(Box, on_delete=models.PROTECT, null=True, blank=True)
    box_position = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    @property
    def get_all_locations(self):
        locations = set()
        for sample in self.samples.all():
            locations.add(sample.location)
        for pool in self.pools.all():
            for sample in pool.samples.all():
                locations.add(sample.location)
        return list(locations)






