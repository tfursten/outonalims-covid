import datetime
from django import forms
from django.forms import ModelForm
from .models import (
    Sample, Project, Location, Researcher, Event, Subject, Box)


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
            'date': DateInput()
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
        fields = ['collection_status', 'box', 'box_position']


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




class FixIDS(forms.Form):
    sample_id = forms.CharField(
        label="Sample ID", max_length=10,
        help_text="Enter sample ID to correct", required=False)
    subject_id = forms.CharField(
        label="Subject ID", max_length=10,
        help_text="Enter subject ID to correct", required=False)
