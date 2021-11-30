from django.db import models
from phone_field import PhoneField
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import datetime
from cualid import create_ids
import uuid
from django.contrib.auth.models import User
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
    dose_1_date = models.DateField(null=True, blank=True)
    dose_2_date = models.DateField(null=True, blank=True)
    booster_date = models.DateField(null=True, blank=True)
    pneumococcal_vaccine = models.BooleanField(null=True, blank=True)
    pneumococcal_date = models.DateField(null=True, blank=True)
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
    size = models.PositiveIntegerField(default=81)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_shelf = models.CharField(max_length=100, blank=True, null=True)
    positions = models.ManyToManyField('SampleBoxPosition', related_name="sample_box")
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on", )
        verbose_name_plural = "sample_boxes"

    def __str__(self):
        return str(self.box_name)

    def number_of_samples_in_box(self):
        count = 0
        for position in self.positions.all():
            if not position.sample == None:
                count += 1
        return count

    def is_full(self):
        if self.number_of_samples_in_box() >= self.size:
            return True
        else:
            return False
    
    def remaining(self):
        return self.size - self.number_of_samples_in_box()

    def get_next_empty_position(self):
        for position in self.positions.all().order_by('position'):
            if position.sample == None:
                return position.id
        return None
            


class PoolBox(models.Model):
    box_name = models.CharField(max_length=100, unique=True)
    size = models.PositiveIntegerField(default=81)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_shelf = models.CharField(max_length=100, blank=True, null=True)
    positions = models.ManyToManyField('PoolBoxPosition', related_name="pool_box")
    created_on = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        ordering = ("-created_on", )
        verbose_name_plural = "pool_boxes"

    def __str__(self):
        return str(self.box_name)

    def number_of_pools_in_box(self):
        count = 0
        for position in self.positions.all():
            if not position.pool == None:
                count += 1
        return count

    def is_full(self):
        if self.number_of_pools_in_box() >= self.size:
            return True
        else:
            return False
    
    def remaining(self):
        return self.size - self.number_of_pools_in_box()

    def get_next_empty_position(self):
        for position in self.positions.all().order_by('position'):
            if position.pool == None:
                return position.id
        return None
    


class SampleBoxPosition(models.Model):
    position = models.PositiveIntegerField()
    sample = models.OneToOneField('Sample', blank=True, null=True, on_delete=models.PROTECT)
    # if no sample, box position is empty
    
    class Meta:
        ordering = ("position",)
        # contrant that prevents duplicate positions
        # constraints = [
        # models.UniqueConstraint(fields=["box", "position"], name='unique position')
        # ]
    
class PoolBoxPosition(models.Model):
    position = models.PositiveIntegerField()
    pool = models.OneToOneField('Pool', blank=True, null=True, on_delete=models.PROTECT)
    # if no Pool, box position is empty
    
    class Meta:
        ordering = ("position",)


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.ManyToManyField(Location)
    researcher = models.ManyToManyField(Researcher, blank=True)
    date = models.DateField()
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
        if SampleBoxPosition.objects.filter(sample=self.id).exists():
            return SampleBoxPosition.objects.filter(sample=self.id)[0]
        else:
            return None

    @property
    def box(self):
        position = self.box_position
        if position:
            box = position.sample_box.all()[0]
            return box
        else:
            return None
    
class Pool(models.Model):
    STATUS_CHOICES = [
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Pending', 'Pending')
    ]
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

    @property
    def get_all_locations(self):
        locations = set()
        for sample in self.samples.all():
            locations.add(sample.location)
        for pool in self.pools.all():
            for sample in pool.samples.all():
                locations.add(sample.location)
        return list(locations)
    
    @property
    def get_all_samples(self):
        samples = set()
        for sample in self.samples.all():
            samples.add(sample)
        for pool in self.pools.all():
            for sample in pool.samples.all():
                samples.add(sample)
        return list(samples)

    @property
    def box_position(self):
        if PoolBoxPosition.objects.filter(pool=self.id).exists():
            return PoolBoxPosition.objects.filter(pool=self.id)[0]
        else:
            return None

    @property
    def box(self):
        position = self.box_position
        if position:
            box = position.pool_box.all()[0]
            return box
        else:
            return None


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
        return str(self.name)


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
        return str(self.name)


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
    



