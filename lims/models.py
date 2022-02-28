import calendar
import uuid
from django.db import models
from phone_field import PhoneField
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import datetime
from cualid import create_ids
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
# 

# require email for users
User._meta.get_field('email').blank = False


class Researcher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=100, unique=True)
    protocol = models.TextField(null=True, blank=True)
    detects = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on", )

    def __str__(self):
        return str(self.name)



class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    investigator = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True) 
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on",)

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
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    
    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):

    SEX_CHOICES = [
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ]
 
    GRADE_CHOICES = [
        ('K', 'K'),
        ('NH', 'NH')
    ]
    GRADE_CHOICES += [(str(i), str(i)) for i in range(1, 13)]
    CONSENT_STATUS = [
        ('Consented', 'Consented'),
        ('Not Consented', 'Not Consented'),
        ('Withdrawn', 'Withdrawn')
    ]
    MONTH_CHOICES = [(m, m) for m in list(calendar.month_name[1:])]

    subject_ui = models.CharField(max_length=6, blank=True, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    consent_status = models.CharField(max_length=15, choices=CONSENT_STATUS, default='Consented')
    consent_date = models.DateField(null=True, blank=True)
    withdrawn_date = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    race = models.ManyToManyField(Race, blank=True)
    ethnicity = models.BooleanField(null=True, blank=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    phone = PhoneField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    gardian_name = models.CharField(max_length=100, null=True, blank=True)
    gardian_relationship = models.CharField(max_length=100, null=True, blank=True)
    teacher_name = models.CharField(max_length=100, null=True, blank=True)
    dose_1 = models.BooleanField(null=True, blank=True)
    dose_2 = models.BooleanField(null=True, blank=True)
    booster = models.BooleanField(null=True, blank=True)
    dose_1_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    dose_1_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    dose_2_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    dose_2_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    booster_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    booster_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    first_covid_case_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    first_covid_case_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    second_covid_case_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    second_covid_case_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    third_covid_case_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    third_covid_case_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    fourth_covid_case_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    fourth_covid_case_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    fifth_covid_case_month = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True, null=True)
    fifth_covid_case_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    pneumococcal_vaccine = models.BooleanField(null=True, blank=True)
    pneumococcal_year = models.PositiveIntegerField(validators=[MinValueValidator(1980)], blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("last_name", "first_name" )
        constraints = [
        models.UniqueConstraint(fields=["first_name", "last_name"], name='unique name')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.subject_ui: # only if subject_ui is blank
            existing_ids = [subj.subject_ui for subj in Subject.objects.all() if subj.subject_ui]
            cualid = create_ids(1, 6, existing_ids=existing_ids)
            self.subject_ui = [cid[0] for cid in cualid][0]
            self.save()
    
    def get_number_of_samples(self, collection_status=None):
        if collection_status == None:
            return len(Sample.objects.filter(subject=self.id))
        else:
            return len(Sample.objects.filter(subject=self.id, collection_status=collection_status))


    def __str__(self):
        return self.subject_ui


class SampleBox(models.Model):
    box_name = models.CharField(max_length=100, unique=True)
    size = models.PositiveIntegerField(default=100)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_shelf = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on", )
        verbose_name_plural = "sample_boxes"

    def __str__(self):
        return str(self.box_name)

    def number_of_samples_in_box(self):
        return self.positions.filter(sample__isnull=False).count()

    def is_full(self):
        return self.number_of_samples_in_box() >= self.size
    
    def remaining(self):
        return self.size - self.number_of_samples_in_box()

    def get_next_empty_position(self):
        next_pos = self.positions.filter(sample__isnull=True).order_by('position').first()
        if next_pos:
            return next_pos.id
        else:
            return None
            


class PoolBox(models.Model):
    box_name = models.CharField(max_length=100, unique=True)
    size = models.PositiveIntegerField(default=100)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_shelf = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on", )
        verbose_name_plural = "pool_boxes"

    def __str__(self):
        return str(self.box_name)

    def number_of_pools_in_box(self):
        return self.positions.filter(pool__isnull=False).count()

    def is_full(self):
        return self.number_of_pools_in_box() >= self.size
    
    def remaining(self):
        return self.size - self.number_of_pools_in_box()

    def get_next_empty_position(self):
        next_pos = self.positions.filter(pool__isnull=True).order_by('position').first()
        if next_pos:
            return next_pos.id
        else:
            return None
     
    


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.ManyToManyField(Location, blank=True)
    researcher = models.ManyToManyField(Researcher, blank=True)
    date = models.DateField()
    week = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-date", )
    
    def __str__(self):
        return str(self.name)

    def get_subjects_at_same_location(self):
        locations = self.location.all()
        subjects = []
        # Grab only consented subjects at same location.
        subjects = Subject.objects.filter(location__in=locations, consent_status="Consented")
        return subjects

    def get_subject_email_list(self):
        subjects = self.get_subjects_at_same_location()
        emails = list(set([subject.email for subject in subjects if subject.email != None]))
        emails = ";".join(emails)
        return emails

    
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
    ('Absent', 'Absent'),
    ('Refused', 'Refused'),
    ('Pending', 'Pending'),
    ('Withdrew', 'Withdrew')
    ]
    SITE = [
        ('Nasal', 'Nasal'),
        ('Oral', 'Oral')
    ]
    name = models.CharField(max_length=6, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    sample_type = models.CharField(max_length=15, choices=SITE, default='Nasal')
    # box = models.ForeignKey(Box, on_delete=models.PROTECT, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)
    # box_position = models.IntegerField(null=True, blank=True)
    collection_event = models.ForeignKey(Event, on_delete=models.PROTECT)
    collection_status = models.CharField(max_length=15, choices=COLLECTION_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    
    class Meta:
        ordering = ("subject", "collection_event", "location", "sample_type")
    
    def __str__(self):
        return str(self.name)

    
    def get_samples_for_event(event, sort_by1="GRADE", sort_by2="LOCATION", sort_by3="NAME", sort_by4="TYPE"):
        sortby = {
            'GRADE': ['subject__grade'],
            'NAME': ['subject__last_name', 'subject__first_name'],
            'LOCATION': ['subject__location'],
            'TYPE': ['sample_type']
            }
        sortby_list = sortby[sort_by1] + sortby[sort_by2] + sortby[sort_by3] + sortby[sort_by4]
        samples = Sample.objects.filter(collection_event=event).order_by(
            *sortby_list)
        return samples

    def get_subjects_at_event(event, sort_by1="grade", sort_by2="location", sort_by3="last_name"):
        """
        Return unique subjects added for an event
        """
        subject_pks = set(
                [sample.subject.id for sample
                in Sample.objects.filter(collection_event=event)])
        subjects = Subject.objects.filter(pk__in=subject_pks).order_by(sort_by1, sort_by2, sort_by3)
        return subjects
      

    def get_subjects_created_at_event(event, sample_type):
        """
        Returns a dictionary of subjects assigned to the same
        location as event. If a subject already has an associated
        sample for this event and sample type it will be listed under
        the 'created' key, otherwise it will be listed under the
        'not_created' key.
        """
        subjects = event.get_subjects_at_same_location()
        subjects_dict = {'created': [], 'not_created': []}
        for subject in subjects:
            # Check if a sample has already been made for this event with this subject
            sample = Sample.objects.filter(
                collection_event=event).filter(
                    subject=subject).filter(
                        sample_type=sample_type)
            if sample.exists():
                subjects_dict['created'].append(subject)
            else:
                subjects_dict['not_created'].append(subject)
        return subjects_dict
   
    @property
    def box_position(self):
        return self.box_samples.all()


    @property
    def box(self):
        position = self.box_position
        return [pos.box for pos in position]
        
    
class Pool(models.Model):
    NOTIFICATION_CHOICES = [
        ('Notified', 'Notified'),
        ('Not Notified', 'Not Notified'),
        ('Pending', 'Pending')
    ]
    name = models.CharField(max_length=100, unique=True)
    samples = models.ManyToManyField(Sample, blank=True)
    pools = models.ManyToManyField('Pool', symmetrical=False, blank=True)
    # result = models.ManyToManyField('TestResult', blank=True)
    # status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    notification_status = models.CharField(max_length=15, choices=NOTIFICATION_CHOICES, default='Pending')
    # box = models.ForeignKey(Box, on_delete=models.PROTECT, null=True, blank=True)
    # box_position = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return str(self.name)


    def get_all_locations(self):
        locations = set()
        for sample in self.samples.all():
            locations.add(sample.location)
        for pool in self.pools.all():
            for sample in pool.samples.all():
                locations.add(sample.location)
        return list(locations)
    
    def get_all_samples(self):
        samples = set()
        for sample in self.samples.all():
            samples.add(sample)
        for pool in self.pools.all():
            for sample in pool.samples.all():
                samples.add(sample)
        return list(samples)
    
    def get_all_subjects(self):
        samples = self.get_all_samples()
        subjects = set()
        for sample in samples:
            subjects.add(sample.subject)
        return list(subjects)

    @property
    def box_position(self):
        return self.box_pools.all()


    @property
    def box(self):
        position = self.box_position
        return [pos.box for pos in position]

    def get_subject_email_list(self):
        subjects = self.get_all_subjects()
        emails = list(set([subject.email for subject in subjects if subject.email != None]))
        emails = ";".join(emails)
        return emails



class SampleBoxPosition(models.Model):
    box = models.ForeignKey(SampleBox, on_delete=models.CASCADE, related_name='positions', null=True, blank=True)
    position = models.PositiveIntegerField()
    sample = models.ForeignKey(
        Sample, blank=True, null=True,
        on_delete=models.SET_NULL, related_name="box_samples")
    # if no sample, box position is empty
    
    class Meta:
        ordering = ("position",)
        # contrant that prevents duplicate positions
        # constraints = [
        # models.UniqueConstraint(fields=["box", "position"], name='unique position')
        # ]
    def __str__(self):
        return str(self.box.box_name) + " " + str(self.position)
    
class PoolBoxPosition(models.Model):
    box = models.ForeignKey(PoolBox, on_delete=models.CASCADE, related_name='positions', null=True, blank=True)
    position = models.PositiveIntegerField()
    pool = models.ForeignKey(
        Pool, blank=True, null=True,
        on_delete=models.SET_NULL, related_name="box_pools")
    # if no Pool, box position is empty
    
    class Meta:
        ordering = ("position",)

    def __str__(self):
        return str(self.box.box_name) + " " + str(self.position)



class SampleResult(models.Model):
    RESULT_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Pending', 'Pending'),
    ('Unknown', 'Unknown'),
    ('Inconclusive', 'Inconclusive')
    ]

    sample = models.ForeignKey(Sample, on_delete=models.PROTECT)
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    replicate = models.PositiveIntegerField(default=1)
    result = models.CharField(max_length=15, choices=RESULT_CHOICES, default='Pending')
    value = models.CharField(max_length=100, null=True, blank=True)
    researcher = models.ManyToManyField(Researcher, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on",)
        # contrant that prevents duplicate sample results
        constraints = [
        models.UniqueConstraint(fields=["sample", "test", "replicate"], name='unique_sample_result')
        ]

    def __str__(self):
        return "{0}_{1}_{2}".format(self.sample.name, self.test, self.replicate)


class PoolResult(models.Model):
    RESULT_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Pending', 'Pending'),
    ('Unknown', 'Unknown'),
    ('Inconclusive', 'Inconclusive')
    ]

    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    replicate = models.PositiveIntegerField(default=1)
    result = models.CharField(max_length=15, choices=RESULT_CHOICES, default='Pending')
    value = models.CharField(max_length=100, null=True, blank=True)
    researcher = models.ManyToManyField(Researcher, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on",)
        # contrant that prevents duplicate pool results
        constraints = [
        models.UniqueConstraint(fields=["pool", "test", "replicate"], name='unique_pool_result')
        ]

    def __str__(self):
        return "{0}_{1}_{2}".format(self.pool.name, self.test, self.replicate)


class Label(models.Model):
    PAPERSIZE_CHOICES = [
    ('LETTER', 'Letter'),
    ]
    name = models.CharField(max_length=100, unique=True)
    paper_size = models.CharField(max_length=15, choices=PAPERSIZE_CHOICES, default='Letter')
    top_margin = models.FloatField()
    left_margin = models.FloatField()
    label_width = models.FloatField()
    label_height = models.FloatField()
    columns = models.PositiveIntegerField()
    rows = models.PositiveIntegerField()
    row_margin = models.FloatField()
    col_margin = models.FloatField()
    top_padding = models.FloatField()
    left_padding = models.FloatField()
    max_chars = models.PositiveIntegerField(default=25)
    font_size = models.FloatField(default=7)
    qr_size = models.FloatField(default=12)
    line_spacing = models.FloatField(default=2.3)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return str(self.name)
    



