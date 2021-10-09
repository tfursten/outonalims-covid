from django import forms
from django.forms import ModelForm
from .models import (
    Sample, Project, Location, Researcher, Event, Subject)


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
        fields = ['subject_ui', 'location', 'first_name',
        'last_name', 'birthdate', 'sex', 'vaccine_status',
        'covid'
        ]
        widgets = {
            'birthdate': DateInput()
        }
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['location'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name