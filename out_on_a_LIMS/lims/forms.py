import datetime
import json
from django import forms
from django.forms import ModelForm, CheckboxInput, SelectMultiple
from .models import (
    Sample, Project, Location, Researcher, Event, Subject, Box, Pool)
from string import capwords
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe

# from django.forms import widgets

class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'investigator',
        'start_date', 'end_date', 'description', 'notes']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }
    
class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'project', 'address',
        'classroom',
        'description', 'contact_name',
        'contact_email', 'contact_phone'
        ]
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['project'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name

class ResearcherForm(ModelForm):
    class Meta:
        model = Researcher
        fields = ['name', 'email', 'phone']


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'date',
        'researcher'
        ]
        widgets = {
            'date': DateInput(),
            'location': forms.SelectMultiple(attrs={'size': '20'})
        }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['location'].label_from_instance = self.label_from_instance
        self.fields['researcher'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['first_name',
        'last_name', 'location', 'age', 'sex', 'race',
        'ethnicity', 'grade', 'phone', 'email',
        'gardian_name', 'gardian_relationship', 
        'teacher_name','vaccine_status', 'dose_1',
        'dose_2', 'dose_3',
        'prior_covid'
        ]
        widgets = {
            'dose_1': DateInput(),
            'dose_2': DateInput(),
            'dose_3': DateInput()
        }
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['location'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['collection_status', 'box', 'box_position', 'notes']


class SamplePrint(forms.Form):
    start_position = forms.IntegerField(min_value=1, initial=1,
        help_text="Change starting position of the labels on the label sheet. Positions start at 1 and increment down each column.")
    replicates = forms.IntegerField(min_value=1, initial=1,
        help_text="Enter the number of labels to print per sample.")
    label_paper = forms.ChoiceField(choices = [('CL-13T1', 'CL-13T1')], initial="CL-13T1")
    sort_by1 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade')], label="Sort by", initial='GRADE')
    sort_by2 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade')], label="Then by", initial="NAME")
    sort_by3 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade')], label="Finally by", initial="LOCATION")

class BoxForm(ModelForm):
    class Meta:
        model = Box
        fields = ['box_name', 'storage_location', 'storage_shelf']


class SelectEventForm(forms.Form):
    today = datetime.date.today()
    # Only select events that have not already completed
    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(date__gte=today),
        help_text="If an event is not listed it is because the event date has passed and event is completed. If the event date is incorrect, you can edit it on the Event page."
        )


class PoolForm(ModelForm):
    class Meta:
        model = Pool
        fields = ['name', 'status', 'box', 'box_position', 'notes']

class PoolUpdateForm(ModelForm):
    class Meta:
        model = Pool
        fields = ['name', 'status', 'box', 'box_position', 'notes', 'samples', 'pools']
    def __init__(self, *args, **kwargs):
        super(PoolUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pools'].queryset = Pool.objects.exclude(id__in=[self.instance.id])


class FixIDS(forms.Form):
    sample_id = forms.CharField(
        label="Sample ID", max_length=10,
        help_text="Enter sample ID to correct", required=False)
    subject_id = forms.CharField(
        label="Subject ID", max_length=10,
        help_text="Enter subject ID to correct", required=False)
