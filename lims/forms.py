import datetime
import json
from django import forms
from django.forms import ModelForm, CheckboxInput, SelectMultiple
from .models import (
    Sample, Project, Location, Researcher,
    Event, Subject, SampleBox, PoolBox,
    SampleBoxPosition, PoolBoxPosition,
     Pool, Label, SampleResult, PoolResult,
    Test)
from string import capwords
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms import widgets



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
        'researcher', 'description', 'notes'
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
        'last_name', 'consent_status', 'consent_date',
        'withdrawn_date',
        'location', 'age', 'sex', 'race',
        'ethnicity', 'grade', 'phone', 'email',
        'gardian_name', 'gardian_relationship', 
        'teacher_name', 'dose_1', 'dose_1_date',
        'dose_2', 'dose_2_date', 'booster', 'booster_date',
        'pneumococcal_vaccine',
        'pneumococcal_date', 'notes'
        ]

        labels = {
            "ethnicity": "Hispanic or Latino/a",
            "dose_1": "COVID-19 Vaccine Dose 1",
            "dose_2": "COVID-19 Vaccine Dose 2",
            "booster": "COVID-19 Vaccine Booster"
        }
        widgets = {
            'consent_date': DateInput(),
            'withdrawn_date': DateInput(),
            'dose_1_date': DateInput(),
            'dose_2_date': DateInput(),
            'booster_date': DateInput(),
            'pneumococcal_date': DateInput(),
            'race': forms.CheckboxSelectMultiple(),
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
        fields = ['collection_status', 'notes']


class SamplePrint(forms.Form):
    start_position = forms.IntegerField(min_value=1, initial=1,
        help_text="Change starting position of the labels on the label sheet. Positions start at 1 and increment down each column.")
    replicates = forms.IntegerField(min_value=1, initial=1,
        help_text="Enter the number of labels to print per sample.")
    label_paper = forms.ModelChoiceField(queryset=Label.objects.all(), initial="CL-6T1")
    sort_by1 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade'), ('TYPE', 'Sample Type')], label="Sort by", initial='GRADE')
    sort_by2 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade'), ('TYPE', 'Sample Type')], label="Then by", initial="NAME")
    sort_by3 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade'), ('TYPE', 'Sample Type')], label="Then by", initial="LOCATION")
    sort_by4 = forms.ChoiceField(choices = [('NAME', 'Subject Name'), ('LOCATION', 'Location'), ('GRADE', 'Grade'), ('TYPE', 'Sample Type')], label="Finally by", initial="TYPE")




class SampleBoxForm(ModelForm):
    class Meta:
        model = SampleBox
        fields = ['box_name', 'size', 'storage_location', 'storage_shelf']
   


class PoolBoxForm(ModelForm):
    class Meta:
        model = PoolBox
        fields = ['box_name', 'size', 'storage_location', 'storage_shelf']


class BoxPositionSampleForm(ModelForm):
    class Meta:
        model = SampleBoxPosition
        fields = ['sample']
    def __init__(self, *args, **kwargs):
        super(BoxPositionSampleForm, self).__init__(*args, **kwargs)
        self.fields['sample'].queryset = Sample.objects.filter(collection_status="Collected").order_by("name")
        


class BoxPositionPoolForm(ModelForm):
    class Meta:
        model = PoolBoxPosition
        fields = ['pool']
    def __init__(self, *args, **kwargs):
        super(BoxPositionPoolForm, self).__init__(*args, **kwargs)
        self.fields['pool'].queryset = Pool.objects.all().order_by("-created_on", "name")


class SelectEventForm(ModelForm):
    class Meta:
        model = Sample
        fields = ['event', 'sample_type']
    today = datetime.date.today()
    # Only select events that have not already completed
    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(date__gte=today),
        help_text="If an event is not listed it is because the event date has passed and event is completed. If the event date is incorrect, you can edit it on the Event page."
        )

    def __init__(self, *args, **kwargs):
        hide_condition = kwargs.pop('hide_type', None)
        super(SelectEventForm, self).__init__(*args, **kwargs)
        if hide_condition:
            del self.fields['sample_type']
 

class SampleNoticeForm(ModelForm):
    initial = """Name: {FIRST_NAME} {LAST_NAME}
Grade: {GRADE}
Teacher: {TEACHER}
_______________________________________________
Please come to <LOCATION> at <TIME> ... 
    """
    today = datetime.date.today()
    # Only select events that have not already completed
    event = forms.ModelChoiceField(
        queryset=Event.objects.filter(date__gte=today),
        help_text="If an event is not listed it is because the event date has passed and event is completed. If the event date is incorrect, you can edit it on the Event page.",
        initial=None)
    notice_text = forms.CharField(widget=forms.Textarea, initial=initial)
    class Meta:
        model = Event
        fields = ['event', 'notice_text']
    def __init__(self, *args, **kwargs):
        super(SampleNoticeForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            if 'event' in kwargs['initial']:
                self.fields['event'].value = kwargs['initial']['event']



class PoolForm(ModelForm):
    class Meta:
        model = Pool
        fields = ['name', 'notification_status', 'notes']

class PoolUpdateForm(ModelForm):
    class Meta:
        model = Pool
        fields = ['name', 'notification_status', 'notes', 'samples', 'pools']
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


class LabelForm(ModelForm):
    class Meta:
        model = Label
        exclude = ['created_on']
    rows = forms.IntegerField(min_value=0, label="Number of Rows")
    columns = forms.IntegerField(min_value=0, label="Number of Columns")
    # paper_size = forms.ChoiceField(label="Paper Size", initial="LETTER")
    top_margin = forms.FloatField(min_value=0.0, label="Margin from top of sheet to first row of labels (mm)")
    left_margin = forms.FloatField(min_value=0.0, label="Margin from left of sheet to first column of labels (mm)")
    label_width = forms.FloatField(min_value=0.0, label="Width of labels (mm)")
    label_height = forms.FloatField(min_value=0.0, label="Height of labels (mm)")
    row_margin = forms.FloatField(min_value=0.0, label="Margin between rows of labels (mm)")
    col_margin = forms.FloatField(min_value=0.0, label="Margin between columns of labels (mm)")
    top_padding = forms.FloatField(label="Padding from label top (mm)")
    left_padding = forms.FloatField(label="Padding from left of label (mm)")
    font_size = forms.FloatField(label="Font size for text", initial=7)
    qr_size = forms.FloatField(min_value=5, label="Size of QR code (mm)", initial=12, help_text="Smaller than 5mm x 5mm will not scan")
    max_chars = forms.IntegerField(min_value=10, label="Maximum number of characters per line", initial=25)
    line_spacing = forms.FloatField(label="Spacing between lines (mm)", initial=2.3)

    
class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'protocol', 'detects']


class SampleResultForm(ModelForm):
    class Meta:
        model = SampleResult
        fields = ['sample', 'test', 'replicate', 'result', 'value', 'notes', 'researcher']
    def __init__(self, *args, **kwargs):
            if 'sample' in kwargs:
                sample = kwargs.pop('sample')
                kwargs.update(initial={
                    'sample': sample
                })
            super(SampleResultForm, self).__init__(*args, **kwargs)
            self.fields['sample'].queryset = Sample.objects.order_by('name')
        

class PoolResultForm(ModelForm):
    class Meta:
        model = PoolResult
        fields = ['pool', 'test', 'replicate', 'result', 'value', 'notes', 'researcher']
    def __init__(self, *args, **kwargs):
            if 'pool' in kwargs:
                pool = kwargs.pop('pool')
                kwargs.update(initial={
                    'pool': pool
                })
            super(PoolResultForm, self).__init__(*args, **kwargs)
            self.fields['pool'].queryset = Pool.objects.order_by('name')

