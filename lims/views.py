import io
import datetime
import json
import time
import hashlib
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, CreateView, DeleteView, UpdateView, DetailView)
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import ProtectedError, Count, Q
from .models import (
    Sample, Project, Location, Researcher, Event,
    Subject, SampleBox, PoolBox, SampleBoxPosition, PoolBoxPosition,
    Pool, Label, Test, SampleResult, PoolResult)
from .forms import (
    ProjectForm, LocationForm, ResearcherForm,
    EventForm, SubjectForm, SampleForm, SampleBoxForm, PoolBoxForm,
    BoxPositionSampleForm, BoxPositionPoolForm,
    SelectEventForm, SamplePrint, PoolForm, PoolUpdateForm, PoolResultSelectTestForm,
    SampleResultSelectTestForm, PoolResultUploadFileForm, SampleResultUploadFileForm,
    LabelForm, TestForm, SampleResultForm, PoolResultForm, FixIDS, SampleNoticeForm, AnalysisSelectionForm)
from cualid import create_ids
import reportlab
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import (LETTER)
from reportlab_qrcode import QRCodeImage
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from difflib import get_close_matches



class SamplePermissionsMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name__in=["Manager", "Staff-Lab"]).exists():
            # Redirect the user to not auth page
            return render(request, 'lims/not_authorized_error.html')
        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)



class SubjectPermissionsMixin(AccessMixin):
    """
    Lab staff does not have permissions to view subject information
    This mixin is placed on all subject info views and redirects
    lab staff to non authorized page.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.groups.filter(name__in=["Manager", "Staff-DataEntry"]).exists():
            # Redirect the user to not auth page
            return render(request, 'lims/not_authorized_error.html')
        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)



def index(request):
    return render(request, 'lims/dashboard.html')


# ============== PROJECTS ================================

class ProjectListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'project_list'
    model = Project


class ProjectFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    template_name_suffix = '_new'
    form_class = ProjectForm
    success_message = "Project was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:project_detail', args=(self.object.id,))


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project

class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    template_name_suffix = '_update'
    form_class = ProjectForm
    success_message = "Project was successfully updated:  %(name)s"
    
    def get_success_url(self):
        return reverse('lims:project_detail', args=(self.object.id,))


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('lims:project_list', args=())
    
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== LOCATIONS ================================

class LocationListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'location_list'
    model = Location


class LocationFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Location
    template_name_suffix = '_new'
    form_class = LocationForm
    success_message = "Location was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:location_detail', args=(self.object.id,))


class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location

class LocationUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Location
    template_name_suffix = '_update'
    form_class = LocationForm
    success_message = "Location was successfully updated:  %(name)s"
    def get_success_url(self):
        return reverse('lims:location_detail', args=(self.object.id,))


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('lims:location_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")


# ============== RESEARCHER ================================


class ResearcherListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'researcher_list'
    model = Researcher


class ResearcherFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Researcher
    template_name_suffix = '_new'
    form_class = ResearcherForm
    success_message = "Researcher was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:researcher_detail', args=(self.object.id,))

class ResearcherDetailView(LoginRequiredMixin, DetailView):
    model = Researcher


class ResearcherUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Researcher
    template_name_suffix = '_update'
    form_class = ResearcherForm
    success_message = "Researcher was successfully updated:  %(name)s"
    def get_success_url(self):
        return reverse('lims:researcher_detail', args=(self.object.id,))


class ResearcherDeleteView(LoginRequiredMixin, DeleteView):
    model = Researcher
    success_url = reverse_lazy('lims:researcher_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== EVENTS ================================
class EventListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'event_list'
    model = Event


class EventFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Event
    template_name_suffix = '_new'
    form_class = EventForm
    success_message = "Event was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:event_detail', args=(self.object.id,))


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event


class EventUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Event
    template_name_suffix = '_update'
    form_class = EventForm
    success_message = "Collection event was successfully updated:  %(name)s"
    def get_success_url(self):
        return reverse('lims:event_detail', args=(self.object.id,))

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('lims:event_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== SUBJECTS ================================

class SubjectListView(SubjectPermissionsMixin, ListView):
    template_name = "lims/subject_list.html"
    model = Subject
    context_object_name = 'subject_list'

    def get_queryset(self):
        return None


@login_required
def subject_list_json_view(request):
    subjects = []
    for subject in Subject.objects.select_related().all():
        data = subject.sample_set.aggregate(
            samples=Count('pk'),
            pending=Count('pk', filter=Q(collection_status='Pending')),
            collected=Count('pk', filter=Q(collection_status="Collected")),
            absent=Count('pk', filter=Q(collection_status="Absent")),
            refused=Count('pk', filter=Q(collection_status="Refused")),
            withdrawn=Count('pk', filter=Q(collection_status="Withdrew"))
            )
        values = {k: v for k, v in subject.__dict__.items() if k in [
            'subject_ui', 'first_name', 'last_name', 'consent_status',
            'grade', 'id']}
        values['location__name'] = subject.location.name
        values['location__id'] = subject.location.id
        data.update(values)
        subjects.append(data)

    
    data = {'data': subjects}
    return JsonResponse(data, safe=False)




class SubjectDetailListView(SubjectPermissionsMixin, ListView):
    template_name_suffix = "_detail_list"
    context_object_name = 'subject_list'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.all()
        all_samples = [subject.get_number_of_samples() for subject in subjects]
        pending_samples = [subject.get_number_of_samples(collection_status="Pending") for subject in subjects]
        collected_samples = [subject.get_number_of_samples(collection_status="Collected") for subject in subjects]
        missed_samples = [subject.get_number_of_samples(collection_status="Absent") for subject in subjects]
        declined_samples = [subject.get_number_of_samples(collection_status="Refused") for subject in subjects]
        context['subject_list'] = zip(
            subjects, all_samples, pending_samples,
            collected_samples, missed_samples, declined_samples)
        return context

    
    def get_queryset(self):
        """
        Return all locations
        """
        return Subject.objects.all()

class SubjectFormView(SuccessMessageMixin, SubjectPermissionsMixin, CreateView):
    model = Subject
    template_name_suffix = '_new'
    form_class = SubjectForm
    
    success_message = "Subject was successfully added"

    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))


class SubjectDetailView(SubjectPermissionsMixin, DetailView):
    model = Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        samples = Sample.objects.filter(subject=self.kwargs['pk'])
        results = []
        for sample in samples:
            
            tests = SampleResult.objects.filter(sample=sample.id)
            if len(tests):
                for test in tests:
                    results.append(
                        [sample.name, sample.id, sample.collection_event.name, sample.collection_event.id,
                        sample.collection_event.date, sample.sample_type,
                        sample.collection_status, test.test.name, test.test.id, test.id,
                        test.result, test.replicate])
            else:
                results.append( 
                    [sample.name, sample.id, sample.collection_event.name,
                    sample.collection_event.id, sample.collection_event.date,
                    sample.sample_type, sample.collection_status, "", "", "",
                    "", ""])


        context['results'] = results
        return context


class SubjectUpdateView(SuccessMessageMixin, SubjectPermissionsMixin, UpdateView):
    model = Subject
    template_name_suffix = '_update'
    form_class = SubjectForm
    success_message = "Subject was successfully updated"
    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))
    

class SubjectDeleteView(SubjectPermissionsMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('lims:subject_list', args=())

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")





# ============== SAMPLES ================================

class SampleListView(SamplePermissionsMixin, ListView):
    template_name = "lims/sample_list.html"
    context_object_name = 'sample_list'
    model = Sample

    def get_queryset(self):
        return None

@login_required
def sample_list_json_view(request):
    samples = Sample.objects.all().values(
        'id', 'name', 'subject__subject_ui', 'subject__id', 'subject__grade',
        'collection_event__name', 'collection_event__id', 'location__name',
        'location__id',
        'collection_status', 'sample_type'
        )
    data = {'data': list(samples)}
    return JsonResponse(data, safe=False)


@login_required
def add_samples(request):
    form = SelectEventForm()
    if request.method == 'POST':
        form = SelectEventForm(request.POST)
        if form.is_valid():
            event = request.POST.get('event')
            sample_type = request.POST.get('sample_type')
            return redirect(
                'lims:verify_new_samples',
                event_id=event, sample_type=sample_type)
    return render(request, 'lims/samples_new.html', {'form':form})


@login_required
def verify_subjects(request, event_id, sample_type):
    event = Event.objects.get(pk=event_id)
    subjects = Sample.get_subjects_created_at_event(event, sample_type)
    if request.method == "GET":
        return render(
            request, 'lims/verify_new_samples.html',
            {'created': subjects['created'],
            'not_created': subjects['not_created'],
            'event_name': event.name, 'sample_type': sample_type})
    elif request.method == "POST":
        n = len(subjects['not_created'])
        size = 6
        # TODO limit unique ids to a project
        existing_ids =[sample.name for sample in Sample.objects.all()]
        cual_ids = [cid[0] for cid in create_ids(n, size, existing_ids=existing_ids)]
        for cual_id, subject in zip(cual_ids, subjects['not_created']):
            # create new samples for subjects that have
            # not been added.
            sample = Sample(name = cual_id, subject=subject, 
                collection_event=event, location=subject.location,
                sample_type=sample_type)
            sample.save(force_insert=True)
        return redirect('lims:event_samples', event_id=event_id)

   

@login_required
def select_event_for_sample(request):
    form = SelectEventForm(hide_type=True)
    if request.method == "POST":
        form = SelectEventForm(request.POST, hide_type=True)
        if form.is_valid():
            event = request.POST.get('event')
            return redirect('lims:sample_labels_options', event_id=event)
    return render(request, 'lims/samples_print_labels_select_event.html', {'form': form})

@login_required
def select_event_for_sample_list(request):
    form = SelectEventForm(hide_type=True)
    if request.method == "POST":
        form = SelectEventForm(request.POST, hide_type=True)
        if form.is_valid():
            event = request.POST.get('event')
            return redirect('lims:subject_list', event_id=event)
    return render(request, 'lims/samples_print_labels.html', {'form': form})

@login_required
def sample_notices(request, event_id=None):
    if event_id:
        form = SampleNoticeForm(initial = {'event': event_id})
    else:
        form = SampleNoticeForm()
    if request.method == "POST":
        form = SelectEventForm(request.POST, hide_type=True)
        if form.is_valid():
            event = request.POST.get('event')
            notice_text = request.POST.get('notice_text')
            return sample_notices_pdf(request, event, notice_text)
    return render(request, 'lims/samples_print_notices.html', {'form': form})

@login_required
def sample_notices_pdf(request, event_id, notice_text):
    buffer = io.BytesIO()
    notice_canvas = canvas.Canvas(buffer, pagesize=LETTER)
    page_width, page_height = LETTER
    event = Event.objects.get(pk=event_id)
    subjects = Sample.get_subjects_at_event(event)
    teachers = [str(subject.teacher_name) for subject in subjects]
    grades = [str(subject.grade) for subject in subjects]
    classrooms = [str(subject.location.classroom) for subject in subjects]
    last_names = [str(subject.last_name) for subject in subjects]
    first_names = [str(subject.first_name) for subject in subjects]
    row = 0
    max_row = 5
    x_start=10
    y_start=(page_height / mm) - 10
    y_space = 55
    for (ln, fn, teacher, grade, classroom) in zip(last_names, first_names, teachers, grades, classrooms):
        y = y_start - (row * y_space)
        textobject = notice_canvas.beginText(x_start * mm, y * mm)
        text = notice_text.format(FIRST_NAME=fn, LAST_NAME=ln, GRADE=grade, TEACHER=teacher, CLASSROOM=classroom)
        for line in text.splitlines(False):
            textobject.textLine(line.rstrip())
        notice_canvas.drawText(textobject)
        notice_canvas.line(0, (y + 10) * mm, page_width, (y + 10) * mm)
        if row < max_row - 1:
            row += 1
        else:
            row = 0
            notice_canvas.showPage()
    notice_canvas.showPage()
    notice_canvas.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename='{}_notices.pdf'.format(event.name.replace(" ", "_").replace(".", "")))



@login_required
def subject_list(request, event_id):
    event = Event.objects.get(pk=event_id)
    subjects = Sample.get_subjects_at_event(event)
    context = {'subjects': subjects, 'event': event}
    return render(request, 'lims/subject_list_for_event.html', context=context)


@login_required
def event_samples(request, event_id):
    event = Event.objects.get(pk=event_id)
    samples = Sample.get_samples_for_event(event)
    context = {'samples': samples, 'event': event}
    return render(request, 'lims/samples_for_event.html', context)


@login_required
def sample_storage_label_options(request):
    form = SamplePrint(initial={
        'label_paper': 3, 'abbreviate': True,
        'sort_by1': 'LOCATION', 'sort_by2': 'EVENT', 'sort_by3': 'GRADE', 'sort_by4': 'NAME' })
    samples = Sample.objects.filter(collection_status="Collected").values(
        'id', 'name', 'subject__subject_ui', 'subject__first_name',
        'subject__last_name', 'subject__grade',
        'collection_event__name', 'location__name',
        'sample_type'
        )
    context = {'data': json.dumps(list(samples)), 'form': form}
    if request.method == "POST":
        form = SamplePrint(request.POST)
        if form.is_valid():
            start_position = request.POST.get('start_position')
            label_paper = request.POST.get('label_paper')
            abbreviate = request.POST.get('abbreviate')
            reps = request.POST.get('replicates')
            sort_by1 = request.POST.get('sort_by1')
            sort_by2 = request.POST.get('sort_by2')
            sort_by3 = request.POST.get('sort_by3')
            sort_by4 = request.POST.get('sort_by4')
            selected_samples = request.POST.getlist('ids')
            return sample_labels_pdf(samples=selected_samples,
                start_position=start_position,
                label_paper=label_paper, abbreviate=abbreviate, replicates=reps,
                sort_by1=sort_by1, sort_by2=sort_by2, sort_by3=sort_by3,
                sort_by4=sort_by4, outfile_name="storage_labels")
    return render(request, 'lims/sample_storage_print_options.html', context=context)   

 

@login_required
def sample_label_options(request, event_id):
    form = SamplePrint(initial={
        'label_paper': 1, 'abbreviate': False,
        'sort_by1': 'GRADE', 'sort_by2': 'NAME', 'sort_by3': 'TYPE', 'sort_by4': 'LOCATION' })
    event = Event.objects.get(pk=event_id)
    samples = Sample.get_samples_for_event(event)
    context = {'samples': samples, 'event': event, 'form': form}
    if request.method == "POST":
        form = SamplePrint(request.POST)
        if form.is_valid():
            start_position = request.POST.get('start_position')
            label_paper = request.POST.get('label_paper')
            abbreviate = request.POST.get('abbreviate')
            reps = request.POST.get('replicates')
            sort_by1 = request.POST.get('sort_by1')
            sort_by2 = request.POST.get('sort_by2')
            sort_by3 = request.POST.get('sort_by3')
            sort_by4 = request.POST.get('sort_by4')
            selected_samples = request.POST.getlist('ids')
            return sample_labels_pdf(samples=selected_samples,
                start_position=start_position,
                label_paper=label_paper, abbreviate=abbreviate, replicates=reps,
                sort_by1=sort_by1, sort_by2=sort_by2, sort_by3=sort_by3,
                sort_by4=sort_by4,
                outfile_name="{}_sample_labels".format(event.name.replace(" ", "_")))
    return render(request, 'lims/sample_print_options.html', context)    


def get_x_y_coordinates(
        columns, rows, left_margin, top_margin,
        label_width, label_height, row_margin, col_margin ):
    x = label_width + col_margin
    y = -(label_height + row_margin)
    for column in range(int(columns)):
        for row in range(int(rows)):
            x_coord = left_margin + (x * column)
            y_coord = top_margin + (y * row)
            yield (x_coord * mm, y_coord * mm)


def sample_labels_pdf(
    samples, start_position,
    label_paper, abbreviate, replicates, sort_by1,
    sort_by2, sort_by3, sort_by4, outfile_name):
    """
    Use Cual-id code to generate labels with barcodes
    """
    # Create a file-like buffer to receive PDF data.
    
    sortby = {
            'GRADE': ['subject__grade'],
            'NAME': ['subject__last_name', 'subject__first_name'],
            'LOCATION': ['subject__location'],
            'TYPE': ['sample_type'],
            'EVENT': ['collection_event__name']
            }
    sortby_list =  sortby[sort_by1] + sortby[sort_by2] + sortby[sort_by3] + sortby[sort_by4]

    label = Label.objects.get(pk=label_paper)
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    paper_size = {'LETTER': LETTER}
    barcode_canvas = canvas.Canvas(buffer, pagesize=paper_size[label.paper_size])
    page_width, page_height = paper_size[label.paper_size]
    columns=label.columns
    rows=label.rows
    x_start=label.left_margin
    y_start=(page_height / mm) - (label.top_margin)
    xy_coords = list(get_x_y_coordinates(
        columns, rows, x_start, y_start,
        label.label_width, label.label_height,
        label.row_margin, label.col_margin))
    c = int(start_position) - 1
    for sample in Sample.objects.filter(pk__in=samples).order_by(*sortby_list).select_related():
        for rep in range(int(replicates)):
            x = xy_coords[c][0] + (label.left_padding * mm)
            y = xy_coords[c][1] - (label.top_padding * mm)
            qr_size = label.qr_size
            qr_code = QRCodeImage(sample.name, size=qr_size * mm)
            qr_code.drawOn(barcode_canvas, x , y - ((qr_size - 4) * mm))
            barcode_canvas.setFont("Helvetica", label.font_size)
            # Add line for last name and first name, cuts off last name before max_chars so that some characters
            # from first name will be included if full name does not fit.
            if abbreviate == "on":
                barcode_canvas.drawString(x + (qr_size * mm), y, "{0} {1}".format(sample.name, sample.sample_type[0]))
                barcode_canvas.drawString(
                    x + (qr_size * mm), (y - (label.line_spacing * mm)), "{0} {1}".format(
                        sample.collection_event.name.replace("Wk", "")[:label.max_chars - 5], str(sample.subject.grade).replace("None", "") ))
            else:
                barcode_canvas.drawString(x + (qr_size * mm), y, "{0} {1}".format(sample.name, sample.sample_type))
                barcode_canvas.drawString(x + (qr_size * mm), (y - (label.line_spacing * mm)), "{0},{1}".format(
                    sample.subject.last_name[:label.max_chars - 2], sample.subject.first_name)[:label.max_chars + 1])
                barcode_canvas.drawString(
                    x + (qr_size * mm), (y - ((label.line_spacing * 2) * mm)), "{0} {1}".format(
                        sample.collection_event.name[:label.max_chars - 5], str(sample.subject.grade).replace("None", "")))
                barcode_canvas.drawString(x + (qr_size * mm), (y - ((label.line_spacing * 3) * mm)), "{0}".format(sample.location.name)[:label.max_chars])
            if c < ((rows*columns) - 1):
                c += 1
            else:
                c = 0
                barcode_canvas.showPage()

    # Close the PDF object cleanly, and we're done.
    barcode_canvas.showPage()
    barcode_canvas.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename="{}.pdf".format(outfile_name))


class SampleDetailView(SamplePermissionsMixin, DetailView):
    model = Sample
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = SampleResult.objects.filter(sample=self.kwargs['pk'])
        context['results'] = results
        return context

class SampleUpdateView(SamplePermissionsMixin, LoginRequiredMixin, UpdateView):
    model = Sample
    template_name_suffix = '_update'
    form_class = SampleForm
    success_message = "Sample was successfully updated"

    def get_success_url(self):
        return reverse('lims:sample_detail', args=(self.object.id,))

# ============== SAMPLE RESULTS ================================

class SampleResultListView(SamplePermissionsMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'result_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample_results = SampleResult.objects.all().values(
        'id', 'sample__collection_event__name', 'sample__collection_event__id',
        'sample__location__id', 'sample__location__name',
        'test__name', 'test__id', 'sample__id', 'sample__name',
        'sample__sample_type', 'replicate', 'result', 'value',
        'notes', 'created_on')

        context['data'] = json.dumps(
            list(sample_results), cls=DjangoJSONEncoder)
        return context

    def get_queryset(self):
        """
        Return all results
        """
        return SampleResult.objects.all()

class SampleResultFormView(SuccessMessageMixin, SamplePermissionsMixin, CreateView):
    model = SampleResult
    template_name_suffix = '_new'
    form_class = SampleResultForm
    success_message = "Sample result was successfully added"

    def get_success_url(self):
        return reverse('lims:sample_result_detail', args=(self.object.id,))


@login_required   
def upload_sample_result_file(request):
    if request.method == 'POST':
        form = SampleResultUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            rep = request.POST.get('replicate')
            researcher = request.POST.get('researcher')
            data = pd.read_excel(
                request.FILES['file'],
                skiprows=23,
                usecols=["Sample", "Target", "Cq"], dtype=str)
            data['id'] = data.index
            data['Sample'] = data['Sample'].apply(lambda x: x.split("_", 1)[0] if Sample.objects.filter(name=x.split("_", 1)[0]).exists() else "Not Found")
            data['Test'] = data['Target'].apply(lambda x: x if Test.objects.filter(name=x).exists() else "Not Found")
            data['Status'] = data['Cq'].apply(lambda x: "Positive" if x.lower() != "undetermined" else "Negative")
            data['Value'] = data['Cq']
            data['Replicate'] = rep
            changes = []

            for n, row in data.iterrows():
                if "Not Found" in row.values:
                    changes.append("Not Added")
                    continue
                sample = Sample.objects.get(name=row.Sample)
                test = Test.objects.get(name=row.Test)
                sample_result, created = SampleResult.objects.update_or_create(
                    sample=sample, test=test, replicate=rep,
                )
                sample_result.result = row.Status
                sample_result.value = row.Value
                if researcher:
                    sample_result.researcher.set(researcher)
                sample_result.save()
                changes.append("Created" if created else "Updated")
            
            data['Changes'] = changes
            data.Changes = pd.Categorical(data.Changes, 
                      categories=["Not Added", "Created", "Updated"],
                      ordered=True)
            data = data[['id', 'Sample', 'Test', 'Replicate', 'Status', 'Value', 'Changes']]
            data = data.sort_values('Changes')
            if "Not Added" in data.Changes.values:
                
                messages.add_message(
                    request,
                    messages.WARNING,
                    '{} records could not be added. Please check and resubmit.'.format(
                        data.Changes.value_counts()['Not Added']
                    ))
            
            data = data.to_json(orient="records")
            
            return render(
                request,
                'lims/sampleresult_upload_complete.html',
                {'data': data})
    else:
        form = SampleResultUploadFileForm()
    return render(request, 'lims/sampleresult_upload.html', {'form': form})



@login_required
def sampleresult_multiple_view(request):
    form = SampleResultSelectTestForm()
    if request.method == 'POST':
        form = SampleResultSelectTestForm(request.POST)
        if form.is_valid():
            test = request.POST.get('test')
            replicate = request.POST.get('replicate')
            return redirect(
                'lims:sampleresult_multiple_add_samples',
                test_id=test, rep=str(replicate))
    return render(request, 'lims/sample_result_multiple.html', {'form':form})


@login_required
def sampleresult_multiple_add_samples(request, test_id, rep):
    test = Test.objects.get(pk=test_id)
    existing_sample_list = [
        sampleresult.sample.id for sampleresult in 
        SampleResult.objects.filter(test=test, replicate=rep)]
    sample_query_set = Sample.objects.filter(
        collection_status="Collected").exclude(
            id__in=existing_sample_list)
    if request.method == 'POST':
        selected_samples = request.POST.getlist('ids')
        for sample_id in selected_samples:
            sample = Sample.objects.get(pk=sample_id)
            result = SampleResult(sample=sample, replicate=int(rep), test=test)
            result.save()
        return redirect(
            'lims:sample_result_list')

    return render(request, 'lims/sampleresult_add_samples.html',
        {'sample_list':sample_query_set})


class SampleResultSampleFormView(SuccessMessageMixin, SamplePermissionsMixin, CreateView):
    model = SampleResult
    template_name_suffix = '_sample_new'
    form_class = SampleResultForm
    success_message = "Sample result was successfully added"

    def get_success_url(self):
        return reverse('lims:sample_result_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(SampleResultSampleFormView, self).get_form_kwargs()
        kwargs['sample'] = self.kwargs['pk']
        return kwargs
    
    def get_success_url(self):
        return reverse('lims:sample_result_detail', args=(self.object.id,))
        


class SampleResultDetailView(SamplePermissionsMixin, DetailView):
    model = SampleResult


class SampleResultUpdateView(SuccessMessageMixin, SamplePermissionsMixin, UpdateView):
    model = SampleResult
    template_name_suffix = '_update'
    form_class = SampleResultForm
    success_message = "Sample result was successfully updated"
    def get_success_url(self):
        return reverse('lims:sample_result_detail', args=(self.object.id,))


class SampleResultDeleteView(SamplePermissionsMixin, DeleteView):
    model = SampleResult
    success_url = reverse_lazy('lims:sample_result_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")


# ============== POOL RESULTS ================================

class PoolResultListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'result_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pool_results = PoolResult.objects.all().values(
            'id', 'test__name', 'test__id', 'pool__id', 'pool__name',
            'replicate', 'result', 'value',
            'notes', 'created_on')

        context['data'] = json.dumps(
            list(pool_results), cls=DjangoJSONEncoder)
        return context

    def get_queryset(self):
        """
        Return all results
        """
        return PoolResult.objects.all()

class PoolResultFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PoolResult
    template_name_suffix = '_new'
    form_class = PoolResultForm
    success_message = "Pool result was successfully added"

    def get_success_url(self):
        return reverse('lims:pool_result_detail', args=(self.object.id,))

@login_required
def poolresult_multiple_view(request):
    form = PoolResultSelectTestForm()
    if request.method == 'POST':
        form = PoolResultSelectTestForm(request.POST)
        if form.is_valid():
            test = request.POST.get('test')
            replicate = request.POST.get('replicate')
            return redirect(
                'lims:poolresult_multiple_add_pools',
                test_id=test, rep=str(replicate))
    return render(request, 'lims/pool_result_multiple.html', {'form':form})


@login_required
def poolresult_multiple_add_pools(request, test_id, rep):
    test = Test.objects.get(pk=test_id)
    existing_pool_list = [
        poolresult.pool.id for poolresult in 
        PoolResult.objects.filter(test=test, replicate=rep)]
    pool_query_set = Pool.objects.all().exclude(id__in=existing_pool_list)

    if request.method == 'POST':
        selected_pools = request.POST.getlist('ids')
        for pool_id in selected_pools:
            pool = Pool.objects.get(pk=pool_id)
            result = PoolResult(pool=pool, replicate=int(rep), test=test)
            result.save()
        return redirect(
            'lims:pool_result_list')

    return render(request, 'lims/poolresult_add_pools.html',
        {'pool_list':pool_query_set})

@login_required   
def upload_pool_result_file(request):
    if request.method == 'POST':
        form = PoolResultUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            rep = request.POST.get('replicate')
            researcher = request.POST.get('researcher')
            data = pd.read_excel(
                request.FILES['file'],
                skiprows=23,
                usecols=["Sample", "Target", "Cq"], dtype=str)
            data['id'] = data.index
            data['Pool'] = data['Sample'].apply(lambda x: x if Pool.objects.filter(name=x).exists() else "Not Found")
            data['Test'] = data['Target'].apply(lambda x: x if Test.objects.filter(name=x).exists() else "Not Found")
            data['Status'] = data['Cq'].apply(lambda x: "Positive" if x.lower() != "undetermined" else "Negative")
            data['Value'] = data['Cq']
            data['Replicate'] = rep
            changes = []

            for n, row in data.iterrows():
                if "Not Found" in row.values:
                    changes.append("Not Added")
                    continue
                pool = Pool.objects.get(name=row.Pool)
                test = Test.objects.get(name=row.Test)
                pool_result, created = PoolResult.objects.update_or_create(
                    pool=pool, test=test, replicate=rep,
                )
                pool_result.result = row.Status
                pool_result.value = row.Value
                if researcher:
                    pool_result.researcher.set(researcher)
                pool_result.save()
                changes.append("Created" if created else "Updated")
            
            data['Changes'] = changes
            data.Changes = pd.Categorical(data.Changes, 
                      categories=["Not Added", "Created", "Updated"],
                      ordered=True)
            data = data[['id', 'Pool', 'Test', 'Replicate', 'Status', 'Value', 'Changes']]
            data = data.sort_values('Changes')
            if "Not Added" in data.Changes.values:
                
                messages.add_message(
                    request,
                    messages.WARNING,
                    '{} records could not be added. Please check and resubmit.'.format(
                        data.Changes.value_counts()['Not Added']
                    ))
            
            data = data.to_json(orient="records")
            
            return render(
                request,
                'lims/poolresult_upload_complete.html',
                {'data': data})
    else:
        form = PoolResultUploadFileForm()
    return render(request, 'lims/poolresult_upload.html', {'form': form})


class PoolResultSampleFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PoolResult
    template_name_suffix = '_pool_new'
    form_class = PoolResultForm
    success_message = "Pool result was successfully added"

    def get_success_url(self):
        return reverse('lims:pool_result_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(PoolResultSampleFormView, self).get_form_kwargs()
        kwargs['pool'] = self.kwargs['pk']
        return kwargs
    
    def get_success_url(self):
        return reverse('lims:pool_result_detail', args=(self.object.id,))
        

class PoolResultDetailView(LoginRequiredMixin, DetailView):
    model = PoolResult


class PoolResultUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PoolResult
    template_name_suffix = '_update'
    form_class = PoolResultForm
    success_message = "Pool result was successfully updated"
    def get_success_url(self):
        return reverse('lims:pool_result_detail', args=(self.object.id,))


class PoolResultDeleteView(LoginRequiredMixin, DeleteView):
    model = PoolResult
    success_url = reverse_lazy('lims:pool_result_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== SAMPLE BOXES ================================
class SampleBoxListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'box_list'

    def get_queryset(self):
        """
        Return all boxes
        """
        return SampleBox.objects.all()

class SampleBoxFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SampleBox
    template_name_suffix = '_new'
    form_class = SampleBoxForm
    success_message = "Storage box was successfully added: %(box_name)s"

    def get_success_url(self):
        return reverse('lims:sample_box_detail', args=(self.object.id,))


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        size = form.cleaned_data['size']
        for pos in range(size):
            box_position = SampleBoxPosition(position=pos+1, box=self.object)
            box_position.save() 
        return HttpResponseRedirect(self.get_success_url()) 

class SampleBoxCopySamples(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SampleBox
    fields = []
    template_name_suffix = '_update_copy'
    success_message = "Samples were successfully copied to sample storage box"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        box_id = self.object.id
        box = SampleBox.objects.get(pk=box_id)
        # Get all boxes of same size
        boxes = SampleBox.objects.filter(size=box.size).exclude(pk=box_id)
        context['box_list'] = boxes
        return context
        
    def post(self, request, *args, **kwargs):
        box = self.get_object()
        # Box selected to copy from
        copy_box = SampleBox.objects.get(pk=int(request.POST.getlist('ids')[0]))
        # copy sample positions from copy box to box.
        copy_box_pos = copy_box.positions.all()
        copy_box_pos_map = {pos.position: pos.sample for pos in copy_box_pos}
        for pos in box.positions.all():
            pos.sample = copy_box_pos_map[pos.position]
            pos.save()
       
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('lims:sample_box_detail', args=(self.object.id,))


class SampleBoxDetailView(LoginRequiredMixin, DetailView):
    model = SampleBox


class SampleBoxUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SampleBox
    template_name_suffix = '_update'
    # form_class = SampleBoxForm
    fields = ['box_name', 'storage_location', 'storage_shelf']
    success_message = "Box was successfully updated:  %(box_name)s"
    def get_success_url(self):
        return reverse('lims:sample_box_detail', args=(self.object.id,))

class SampleBoxDeleteView(LoginRequiredMixin, DeleteView):
    model = SampleBox
    success_url = reverse_lazy('lims:sample_box_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")




# ============== POOL BOXES ================================
class PoolBoxListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'box_list'

    def get_queryset(self):
        """
        Return all boxes
        """
        return PoolBox.objects.all()

class PoolBoxFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PoolBox
    template_name_suffix = '_new'
    form_class = PoolBoxForm
    success_message = "Storage box was successfully added"

    def get_success_url(self):
        return reverse('lims:pool_box_detail', args=(self.object.id,))


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        size = form.cleaned_data['size']
        for pos in range(size):
            box_position = PoolBoxPosition(position=pos+1)
            box_position.save()
            self.object.positions.add(box_position)
        self.object.save()
        form.save_m2m() 
        return HttpResponseRedirect(self.get_success_url()) 


class PoolBoxDetailView(LoginRequiredMixin, DetailView):
    model = PoolBox


class PoolBoxUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PoolBox
    template_name_suffix = '_update'
    # form_class = PoolBoxForm
    fields = ['box_name', 'storage_location', 'storage_shelf']
    success_message = "Box was successfully updated:  %(box_name)s"
    def get_success_url(self):
        return reverse('lims:pool_box_detail', args=(self.object.id,))

class PoolBoxDeleteView(LoginRequiredMixin, DeleteView):
    model = PoolBox
    success_url = reverse_lazy('lims:pool_box_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== BOX POSITIONS ================================
class SampleBoxPosDetailView(LoginRequiredMixin, DetailView):
    model = SampleBoxPosition


class SampleBoxPositionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SampleBoxPosition
    template_name_suffix = '_update'
    form_class = BoxPositionSampleForm
    success_message = "Box position was successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(SampleBoxPositionUpdateView, self).get_context_data(**kwargs)
        box = SampleBox.objects.get(id=self.kwargs.get('pk_box', ''))
        context['samplebox'] = box
        return context
    
    def get_success_url(self):
        return reverse('lims:sample_box_detail', args=(self.get_context_data()['samplebox'].id,))


class SampleBoxPositionContinuousUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SampleBoxPosition
    template_name_suffix = '_update_continuous'
    form_class = BoxPositionSampleForm
    success_message = "Box position was successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(SampleBoxPositionContinuousUpdateView, self).get_context_data(**kwargs)
        box = SampleBox.objects.get(id=self.kwargs.get('pk_box', ''))
        context['samplebox'] = box
        return context
    
    def get_success_url(self):
        next_position = self.get_context_data()['samplebox'].get_next_empty_position()
        print("NEXT POS: ", next_position)
        if next_position:
            print("NEXT POSITION")
            return reverse(
                'lims:edit_sample_box_position_continuous',
                args=(self.get_context_data()['samplebox'].id,
                self.get_context_data()['samplebox'].get_next_empty_position()))
        else:
            if 'newbox' in self.request.POST:
                # add new sample box when full
                return reverse('lims:new_sample_box')
            else:
                return reverse('lims:sample_box_list')


class PoolBoxPosDetailView(LoginRequiredMixin, DetailView):
    model = PoolBoxPosition

    def get_context_data(self, **kwargs):
        context = super(PoolBoxPosDetailView, self).get_context_data(**kwargs)
        box = PoolBox.objects.get(id=self.kwargs.get('pk_box', ''))
        context['poolbox'] = box
        return context


class PoolBoxPositionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PoolBoxPosition
    template_name_suffix = '_update'
    form_class = BoxPositionPoolForm
    success_message = "Box position was successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(PoolBoxPositionUpdateView, self).get_context_data(**kwargs)
        box = PoolBox.objects.get(id=self.kwargs.get('pk_box', ''))
        context['poolbox'] = box
        return context
    
    def get_success_url(self):
        return reverse('lims:pool_box_detail', args=(self.get_context_data()['poolbox'].id,))

class PoolBoxPositionContinuousUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PoolBoxPosition
    template_name_suffix = '_update_continuous'
    form_class = BoxPositionPoolForm
    success_message = "Box position was successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(PoolBoxPositionContinuousUpdateView, self).get_context_data(**kwargs)
        box = PoolBox.objects.get(id=self.kwargs.get('pk_box', ''))
        context['poolbox'] = box
        return context
    
    def get_success_url(self):
        next_position = self.get_context_data()['poolbox'].get_next_empty_position()
        if next_position:
            return reverse(
                'lims:edit_pool_box_position_continuous',
                args=(self.get_context_data()['poolbox'].id,
                self.get_context_data()['poolbox'].get_next_empty_position()))
        
        else:
            if 'newbox' in self.request.POST:
                # add new sample box when full
                return reverse('lims:new_pool_box')
            else:
                return reverse('lims:pool_box_list')




# ============== POOLS ================================
class PoolListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'pool_list'

    def get_queryset(self):
        """
        Return all pools
        """
        return Pool.objects.all()

class PoolFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Pool
    template_name_suffix = '_new'
    form_class = PoolForm
    success_message = "Pool was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:pool_detail', args=(self.object.id,))

class PoolAddSamples(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Pool
    fields = []
    template_name_suffix = '_add_samples'
    success_message = "Samples were successfully added to pool"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        samples = Sample.objects.filter(collection_status="Collected").values(
        'id', 'name',
        'collection_event__name', 'location__name',
        'collection_status', 'sample_type'
        )
        context['data'] = list(samples)
        return context
        
    def post(self, request, *args, **kwargs):
        pool = self.get_object()
        samples = [Sample.objects.get(pk=int(sample)) for sample in request.POST.getlist('ids')]
        for sample in samples:
            pool.samples.add(sample)
        pool.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('lims:pool_detail', args=(self.object.id,))


class PoolAddPools(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Pool
    fields = []
    template_name_suffix = '_add_pools'
    success_message = "Pools were successfully added to pool"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pool_id = self.object.id
        # Get all pools that are not current pool
        pools = Pool.objects.exclude(pk=pool_id).values(
            'id', 'name'
        )
        context['data'] = list(pools)
        return context
        
    def post(self, request, *args, **kwargs):
        pool = self.get_object()
        pools = [Pool.objects.get(pk=int(p)) for p in request.POST.getlist('ids')]
        for p in pools:
            pool.pools.add(p)
        pool.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('lims:pool_detail', args=(self.object.id,))


class PoolDetailView(LoginRequiredMixin, DetailView):
    model = Pool
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = PoolResult.objects.filter(pool=self.kwargs['pk'])
        context['results'] = results
        return context


class PoolReportDetailView(SubjectPermissionsMixin, DetailView):
    model = Pool
    template_name_suffix = "_report_detail"


class PoolUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Pool
    template_name_suffix = '_update'
    form_class = PoolUpdateForm
    success_message = "Pool was successfully updated:  %(name)s"

    def get_success_url(self):
        return reverse('lims:pool_detail', args=(self.object.id,))

class PoolDeleteView(LoginRequiredMixin, DeleteView):
    model = Pool
    success_url = reverse_lazy('lims:pool_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== LABELS =================================

class LabelListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'label_list'

    def get_queryset(self):
        """
        Return all labels
        """
        return Label.objects.all()


class LabelFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    template_name_suffix = '_new'
    form_class = LabelForm
    success_message = "Label format was successfully added: %(name)s"


    def get_success_url(self):
        return reverse('lims:label_detail', args=(self.object.id,))
        

class LabelDetailView(LoginRequiredMixin, DetailView):
    model = Label


class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    template_name_suffix = '_update'
    form_class = LabelForm
    success_message = "Label format was successfully updated:  %(name)s"
    
    def get_success_url(self):
        return reverse('lims:label_detail', args=(self.object.id,))

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('lims:label_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")


# ============== TESTS =================================

class TestListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'test_list'

    def get_queryset(self):
        """
        Return all tests
        """
        return Test.objects.all()


class TestFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Test
    template_name_suffix = '_new'
    form_class = TestForm
    success_message = "Test was successfully added: %(name)s"


    def get_success_url(self):
        return reverse('lims:test_detail', args=(self.object.id,))
        

class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test


class TestUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Test
    template_name_suffix = '_update'
    form_class = TestForm
    success_message = "Test was successfully updated:  %(name)s"
    
    def get_success_url(self):
        return reverse('lims:test_detail', args=(self.object.id,))

class TestDeleteView(LoginRequiredMixin, DeleteView):
    model = Test
    success_url = reverse_lazy('lims:test_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")


# ============== ANALYSIS =================================

@login_required
def select_analysis_view(request):
    form = AnalysisSelectionForm()
    if request.method == 'POST':
        form = AnalysisSelectionForm(request.POST)
        if form.is_valid():
            return redirect(
                'lims:analysis_data',
                test=request.POST.get('test'),
                project=request.POST.get('project'))
    return render(request, 'lims/analysis_select.html', {'form': form})



def sample_storage_label_options(request):
    form = SamplePrint(initial={
        'label_paper': 3, 'abbreviate': True,
        'sort_by1': 'LOCATION', 'sort_by2': 'EVENT', 'sort_by3': 'GRADE', 'sort_by4': 'NAME' })
    samples = Sample.objects.filter(collection_status="Collected").values(
        'id', 'name', 'subject__subject_ui', 'subject__first_name',
        'subject__last_name', 'subject__grade',
        'collection_event__name', 'location__name',
        'sample_type'
        )
    context = {'data': json.dumps(list(samples)), 'form': form}
    if request.method == "POST":
        form = SamplePrint(request.POST)
        if form.is_valid():
            start_position = request.POST.get('start_position')
            label_paper = request.POST.get('label_paper')
            abbreviate = request.POST.get('abbreviate')
            reps = request.POST.get('replicates')
            sort_by1 = request.POST.get('sort_by1')
            sort_by2 = request.POST.get('sort_by2')
            sort_by3 = request.POST.get('sort_by3')
            sort_by4 = request.POST.get('sort_by4')
            selected_samples = request.POST.getlist('ids')
            return sample_labels_pdf(samples=selected_samples,
                start_position=start_position,
                label_paper=label_paper, abbreviate=abbreviate, replicates=reps,
                sort_by1=sort_by1, sort_by2=sort_by2, sort_by3=sort_by3,
                sort_by4=sort_by4, outfile_name="storage_labels")
    return render(request, 'lims/sample_storage_print_options.html', context=context)   




@login_required
def analysis_data_view(request, test, project):
    results = []
    # Get number of events
    project = Project.objects.get(pk=project)
    test = Test.objects.get(pk=test)
    events = Event.objects.all().values_list("week", flat=True).order_by('week').distinct()
    results = SampleResult.objects.select_related().filter(test=test, sample__subject__location__project=project).values(
        'sample__subject__location__project__name',
        'sample__subject__subject_ui',
        'sample__subject__location__name',
        'sample__subject__age',
        'sample__subject__sex',
        'sample__subject__ethnicity',
        'sample__subject__grade',
        'sample__subject__dose_1',
        'sample__subject__dose_2',
        'sample__subject__booster',
        'sample__subject__dose_1_month',
        'sample__subject__dose_1_year',
        'sample__subject__dose_2_month',
        'sample__subject__dose_2_year',
        'sample__subject__booster_month',
        'sample__subject__booster_year',
        'sample__subject__first_covid_case_month',
        'sample__subject__first_covid_case_year',
        'sample__subject__second_covid_case_month',
        'sample__subject__second_covid_case_year',
        'sample__subject__third_covid_case_month',
        'sample__subject__third_covid_case_year',
        'sample__subject__fourth_covid_case_month',
        'sample__subject__fourth_covid_case_year',
        'sample__subject__fifth_covid_case_month',
        'sample__subject__fifth_covid_case_year',
        'sample__subject__pneumococcal_vaccine',
        'sample__subject__pneumococcal_year',
        'sample__subject__created_on',
        'sample__subject__consent_status',
        'sample__collection_event__week',
        'sample__sample_type',
        'test__name',
        'replicate',
        'result'
        )
    df = pd.DataFrame(results)
    race_map = {
        sub.subject_ui: "/ ".join([str(r.name) for r in sub.race.all()])
        for sub in Subject.objects.select_related().all()}
    df['race'] = df['sample__subject__subject_ui'].apply(lambda x: race_map.get(x, None))
    


    # Check if multiple samples are collected in same week, outside of different sample types and 
    # Replicate results. 
    df['Sample_Rep'] = 1
    for n, d in df.groupby(
        ['sample__collection_event__week', 'sample__subject__subject_ui', 'sample__sample_type', 'replicate']):
        for i, row in enumerate(d.index):
            df.loc[row, 'Sample_Rep'] += i
  
    df['sample__collection_event__week'] = df['sample__collection_event__week'].apply(
        lambda x: "Week_{}".format(x))

    pdf = df.pivot(
        values='result',
        columns=['sample__collection_event__week', 'sample__sample_type', 'replicate', 'Sample_Rep'],
        index=[
        'sample__subject__location__project__name',
        'test__name',
        'sample__subject__subject_ui',
        'sample__subject__location__name',
        'sample__subject__age',
        'sample__subject__sex',
        'race',
        'sample__subject__ethnicity',
        'sample__subject__grade',
        'sample__subject__dose_1',
        'sample__subject__dose_2',
        'sample__subject__booster',
        'sample__subject__dose_1_month',
        'sample__subject__dose_1_year',
        'sample__subject__dose_2_month',
        'sample__subject__dose_2_year',
        'sample__subject__booster_month',
        'sample__subject__booster_year',
        'sample__subject__first_covid_case_month',
        'sample__subject__first_covid_case_year',
        'sample__subject__second_covid_case_month',
        'sample__subject__second_covid_case_year',
        'sample__subject__third_covid_case_month',
        'sample__subject__third_covid_case_year',
        'sample__subject__fourth_covid_case_month',
        'sample__subject__fourth_covid_case_year',
        'sample__subject__fifth_covid_case_month',
        'sample__subject__fifth_covid_case_year',
        'sample__subject__pneumococcal_vaccine',
        'sample__subject__pneumococcal_year',
        'sample__subject__created_on',
        'sample__subject__consent_status',
    
        ])
    pdf = pdf.replace({'Negative': 0, 'Positive': 1, 'Pending': -1,
        np.nan: -1, 'Unknown':-1, 'Inconclusive': -1})
    pdf = pdf.reset_index()

    column_map = {
        'race': "Race",
        'test__name': "Test",
        'sample__subject__age': "Age",
        'sample__subject__booster': "COVID-19 Vaccine Booster",
        'sample__subject__booster_month': "COVID-19 Vaccine Booster Month",
        'sample__subject__booster_year': "COVID-19 Vaccine Booster Booster Year",
        'sample__subject__consent_status': "Consent Status",
        'sample__subject__created_on': "Created On",
        'sample__subject__dose_1': "COVID-19 Vaccine Dose 1",
        'sample__subject__dose_1_month': "COVID-19 Vaccine Dose 1 Month",
        'sample__subject__dose_1_year': "COVID-19 Vaccine Dose 1 Year",
        'sample__subject__dose_2': "COVID-19 Vaccine Dose 2",
        'sample__subject__dose_2_month': "COVID-19 Vaccine Dose 2 Month",
        'sample__subject__dose_2_year': "COVID-19 Vaccine Dose 2 Year",
        'sample__subject__ethnicity': "Hispanic",
        'sample__subject__subject_ui': "Subject ID",
        'sample__subject__fifth_covid_case_month': "COVID-19 5th Case Month",
        'sample__subject__fifth_covid_case_year': "COVID-19 5th Case Year",
        'sample__subject__first_covid_case_month': "COVID-19 1st Case Month",
        'sample__subject__first_covid_case_year': "COVID-19 1st Case Year",
        'sample__subject__fourth_covid_case_month': "COVID-19 4th Case Month",
        'sample__subject__fourth_covid_case_year': "COVID-19 4th Case Year",
        'sample__subject__grade': "Grade",
        'sample__subject__location__name': "Location",
        'sample__subject__location__project__name': "Project",
        'sample__subject__pneumococcal_vaccine': "Pneumococcal Vaccine",
        'sample__subject__pneumococcal_year': "Pneumococcal Vaccine Year",
        'sample__subject__second_covid_case_month': "COVID-19 2nd Case Month",
        'sample__subject__second_covid_case_year': "COVID-19 2nd Case Year",
        'sample__subject__sex': "Sex",
        'sample__subject__third_covid_case_month': "COVID-19 3rd Case Month",
        'sample__subject__third_covid_case_year': "COVID-19 3rd Case Year",
    
    }
    pdf.columns = ["_".join(map(str, c)).rstrip("_")
        for c in pdf.columns.values]
    pdf['sample__subject__created_on'] = df['sample__subject__created_on'].dt.strftime('%Y-%m-%d')
    # Add headers without results
    headers = [ 
        {'data': h, 'title': column_map.get(h, h)} 
        for h in pdf.columns.values if "Week" not in h]
    # sort results
    def get_sorting_values(x):
        vals = x.split("_")
        vals[1] = int(vals[1])
        vals[3] = int(vals[3])
        vals[4] = int(vals[4])
        return vals
    [headers.append({'data': h, 'title': h})
        for h in sorted([hh for hh in pdf.columns.values if "Week" in hh],
        key=get_sorting_values)]


    context = {'data': pdf.to_json(orient="records"),
    'project': project, 'test': test, 'headers': headers}
    return render(request, 'lims/analysis_table.html', context=context)
   

# ============== HELP =================================


def help(request):
    return render(request, 'lims/help.html')

# ============== FIX IDS =================

def fix_cualid_function(existing_ids, check_id, thresh=0.5):
    if not check_id:
        # if there was no id to check
        return ''
    fixed_id = get_close_matches(check_id, existing_ids, 1, thresh)
    if not len(fixed_id):
        fixed_id = 'Cannot Correct ID!'
    else:
        fixed_id = fixed_id[0]
    return fixed_id


def fix_ids(request):
    form = FixIDS()
    if request.method == "POST":
        form = FixIDS(request.POST)
        if form.is_valid():
            sample_id = request.POST.get('sample_id')
            subject_id = request.POST.get('subject_id')
            existing_sample_ids = [s.name for s in Sample.objects.all()]
            existing_subject_ids = [s.subject_ui for s in Subject.objects.all()]
            fixed_sample = fix_cualid_function(existing_sample_ids, sample_id)
            fixed_subject = fix_cualid_function(existing_subject_ids, subject_id)
            return render(request, 'lims/fix_ids.html', {
                'form': form,
                'fixed_sample': fixed_sample,
                'fixed_subject': fixed_subject})
            
    return render(request, 'lims/fix_ids.html', {'form': form})



def search_view(request):
    code = request.GET.get('code')
    sample = Sample.objects.filter(name=code)
    if len(sample):
        return redirect('lims:sample_detail', pk=int(sample[0].id))
    else:
        return render(request, 'lims/sample_not_found.html', {'sample': code})

  

@login_required
def sample_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        json_response = {"data": []}
        samples = []
        statuses = []
        for k, v in request.POST.items():
            if "collection_status" in k:
                collection_status = v
                sample_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                try:
                    sample = Sample.objects.get(pk=sample_id)
                except Sample.DoesNotExist:
                    return render(request, "lims/sample_not_found.html")
                ori_post = request.POST.copy()
                ori_post['collection_status'] = collection_status
                ori_post['instance'] = sample
                form = SampleForm(ori_post)
                if form.is_valid():
                    samples.append(sample)
                    statuses.append(collection_status)
                    json_response['data'].append({
                            "id": str(sample_id),
                            "name": ori_post['data[{}][name]'.format(sample_id)],
                            "subject__subject_ui": ori_post['data[{}][subject__subject_ui]'.format(sample_id)],
                            "collection_event__name": ori_post['data[{}][collection_event__name]'.format(sample_id)],
                            "collection_event__id": str(sample.collection_event.id),
                            "location__name": ori_post['data[{}][location__name]'.format(sample_id)],
                            "location__id": str(sample.location.id),
                            "collection_status": collection_status,
                            "sample_type": str(sample.sample_type)
                        })
                else:
                    return JsonResponse({"error": str(form.errors)})
        for sample, status in zip(samples, statuses):
            sample.collection_status = status
            sample.save()
            
        return JsonResponse(json_response)


@login_required
def pool_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        json_response = {"data": []}
        pools = []
        statuses = []
        for k, v in request.POST.items():
            if "notification_status" in k:
                notification_status = v
                pool_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                try:
                    pool = Pool.objects.get(pk=pool_id)
                except Pool.DoesNotExist as e:
                    return JsonResponse({"error": str(e)})
                ori_post = request.POST.copy()
                ori_post['notification_status'] = notification_status
                ori_post['name'] = pool.name
                form = PoolForm(ori_post, instance=pool)
                if form.is_valid():
                    pools.append(pool)
                    statuses.append(notification_status)
                    json_response['data'].append({
                            "DT_RowId": str(pool_id),
                            "name": ori_post['data[{}][name]'.format(pool_id)],
                            "notification_status": notification_status,
                        })
                else:
                    return JsonResponse({"error": str(form.errors)})
        for pool, status in zip(pools, statuses):
            pool.notificaiton_status = status
            pool.save()
            
        return JsonResponse(json_response)


@login_required
def poolbox_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        update_values = {}
        # pull values from request
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in update_values:
                    update_values[row_id] = {}
                if "location" in k:
                    update_values[row_id]['location'] = v
                elif "shelf" in k:
                    update_values[row_id]['shelf'] = v
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id in update_values.keys():
            try:
                pool_box = PoolBox.objects.get(pk=object_id)
                update_values[object_id]['object'] = pool_box
            except PoolBox.DoesNotExist as e:
                return JsonResponse({"error": str(e)})
        # Form validation
        json_response = {"data": []}
        for obj_id, vals in update_values.items():
            ori_post = request.POST.copy()
            # add box name as it is required for form validation
            ori_post['box_name'] = vals['object'].box_name
            ori_post['size'] = vals['object'].size
            for k, v in vals.items():
                if k != 'object':
                    ori_post[k] = v
            form = PoolBoxForm(ori_post, instance=vals['object'])
            if form.is_valid():
                json_response['data'].append({
                        "DT_RowId": str(obj_id),
                        "box_id": ori_post['data[{}][box_id]'.format(obj_id)],
                        "available_space": ori_post['data[{}][available_space]'.format(obj_id)],
                        "n_pools": ori_post['data[{}][n_pools]'.format(obj_id)],
                        "size": ori_post['data[{}][size]'.format(obj_id)],
                        "location": vals['location'],
                        "shelf": vals['shelf']
                    })
            else:
                return JsonResponse({"error": str(form.errors)})
        # Update database
        for obj_id, vals in update_values.items():
            poolbox = vals['object']
            poolbox.storage_location = vals['location']
            poolbox.storage_shelf = vals['shelf']
            poolbox.save()
            
        return JsonResponse(json_response)


@login_required
def samplebox_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        update_values = {}
        # pull values from request
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in update_values:
                    update_values[row_id] = {}
                if "location" in k:
                    update_values[row_id]['location'] = v
                elif "shelf" in k:
                    update_values[row_id]['shelf'] = v
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id in update_values.keys():
            try:
                sample_box = SampleBox.objects.get(pk=object_id)
                update_values[object_id]['object'] = sample_box
            except SampleBox.DoesNotExist as e:
                return JsonResponse({"error": str(e)})
        # Form validation
        json_response = {"data": []}
        for obj_id, vals in update_values.items():
            ori_post = request.POST.copy()
            # add box name as it is required for form validation
            ori_post['box_name'] = vals['object'].box_name
            ori_post['size'] = vals['object'].size
            for k, v in vals.items():
                if k != 'object':
                    ori_post[k] = v
            form = SampleBoxForm(ori_post, instance=vals['object'])
            if form.is_valid():
                json_response['data'].append({
                        "DT_RowId": str(obj_id),
                        "box_id": ori_post['data[{}][box_id]'.format(obj_id)],
                        "available_space": ori_post['data[{}][available_space]'.format(obj_id)],
                        "n_samples": ori_post['data[{}][n_samples]'.format(obj_id)],
                        "size": ori_post['data[{}][size]'.format(obj_id)],
                        "location": vals['location'],
                        "shelf": vals['shelf']
                    })
            else:
                return JsonResponse({"error": str(form.errors)})
        # Update database
        for obj_id, vals in update_values.items():
            samplebox = vals['object']
            samplebox.storage_location = vals['location']
            samplebox.storage_shelf = vals['shelf']
            samplebox.save()
            
        return JsonResponse(json_response)


@login_required
def sampleresults_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        update_values = {}
        # pull values from request
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in update_values:
                    update_values[row_id] = {}
                if "result" in k:
                    update_values[row_id]['result'] = v
                elif "value" in k:
                    update_values[row_id]['value'] = v
                elif "notes" in k:
                    update_values[row_id]['notes'] = v
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id in update_values.keys():
            try:
                sample_result = SampleResult.objects.get(pk=object_id)
                update_values[object_id]['object'] = sample_result
            except SampleResult.DoesNotExist as e:
                return JsonResponse({"error": str(e)})
        # Form validation
        json_response = {"data": []}
        for obj_id, vals in update_values.items():
            ori_post = request.POST.copy()
            ori_post['sample'] = vals['object'].sample
            ori_post['test'] = vals['object'].test
            ori_post['replicate'] = vals['object'].replicate
            for k, v in vals.items():
                if k != 'object':
                    ori_post[k] = v

            form = SampleResultForm(ori_post, instance=vals['object'])

            if form.is_valid():
                data = SampleResult.objects.filter(pk=obj_id).values(
                    'id', 'sample__collection_event__name', 'sample__collection_event__id',
                    'sample__location__id', 'sample__location__name',
                    'test__name', 'test__id', 'sample__id', 'sample__name',
                    'sample__sample_type', 'replicate', 'created_on', 'result',
                    'value', 'notes')[0]
                data['result'] = vals['result']
                data['value'] = vals['value']
                data['notes'] = vals['notes']

                json_response['data'].append(data)
            else:
                return JsonResponse({"error": str(form.errors)})
        # Update database
        for obj_id, vals in update_values.items():
            sampleresult = vals['object']
            sampleresult.result = vals['result']
            sampleresult.value = vals['value']
            sampleresult.notes = vals['notes']
            sampleresult.save()
            
        return JsonResponse(json_response)

@login_required
def poolresults_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        update_values = {}
        # pull values from request
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in update_values:
                    update_values[row_id] = {}
                if "result" in k:
                    update_values[row_id]['result'] = v
                elif "value" in k:
                    update_values[row_id]['value'] = v
                elif "notes" in k:
                    update_values[row_id]['notes'] = v
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id in update_values.keys():
            try:
                pool_result = PoolResult.objects.get(pk=object_id)
                update_values[object_id]['object'] = pool_result
            except PoolResult.DoesNotExist as e:
                return JsonResponse({"error": str(e)})
        # Form validation
        json_response = {"data": []}
        for obj_id, vals in update_values.items():
            ori_post = request.POST.copy()
            ori_post['pool'] = vals['object'].pool
            ori_post['test'] = vals['object'].test
            ori_post['replicate'] = vals['object'].replicate
            for k, v in vals.items():
                if k != 'object':
                    ori_post[k] = v
            
            form = PoolResultForm(ori_post, instance=vals['object'])
            if form.is_valid():
                data = PoolResult.objects.filter(pk=obj_id).values(
                    'id', 'test__name', 'test__id', 'pool__name', 'pool__id',
                    'replicate', 'result', 'value', 'notes', 'created_on'
                )[0]
                data['result'] = vals['result']
                data['value'] = vals['value']
                data['notes'] = vals['notes']
                
                
                json_response['data'].append(data)
            else:
                return JsonResponse({"error": str(form.errors)})
        # Update database
        for obj_id, vals in update_values.items():
            poolresult = vals['object']
            poolresult.result = vals['result']
            poolresult.value = vals['value']
            poolresult.notes = vals['notes']
            poolresult.save()
            
        return JsonResponse(json_response)


@login_required
def events_table_update_view(request):
    if (request.method == "POST") and (request.POST.get('action') == "edit"):
        update_values = {}
        # pull values from request
        print("POST", request.POST)
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in update_values:
                    update_values[row_id] = {}
                if "collection_date" in k:
                    update_values[row_id]['date'] = v
                if "week" in k:
                    update_values[row_id]['week'] = v
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id in update_values.keys():
            try:
                event = Event.objects.get(pk=object_id)
                update_values[object_id]['object'] = event
            except Event.DoesNotExist as e:
                return JsonResponse({"error": str(e)})
        # Form validation
        for obj_id, vals in update_values.items():
            ori_post = request.POST.copy()
            # add event name and week as it is required for form validation
            ori_post['name'] = vals['object'].name
            ori_post['week'] = vals
            for k, v in vals.items():
                if k != 'object':
                    print(k, v)
                    ori_post[k] = v
            form = EventForm(ori_post, instance=vals['object'])
            if not form.is_valid():
                return JsonResponse({"error": str(form.errors)})
                
        # Update database
        json_response = {"data": []}

        for obj_id, vals in update_values.items():
            event = vals['object']
            event.date = datetime.datetime.strptime(vals['date'], '%Y-%m-%d').date()
            event.save()
            status = "Completed" if event.is_complete else "Pending"
            json_response['data'].append({
                        "DT_RowId": str(obj_id),
                        "event_name": ori_post['data[{}][event_name]'.format(obj_id)],
                        "event_status": status,
                        "collection_date": event.date,
                        "week": event.week
                    })

            
        return JsonResponse(json_response)


@login_required
def pooladdsamples_table_update_view(request):
    # verify that the post is a remove action

    if (request.method == "POST") and (request.POST.get('action') == 'remove'):
        delete_values = {}
        # pull values from request
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in delete_values:
                    delete_values[row_id] = {}
                if "pool_name" in k:
                    delete_values[row_id]['pool_name'] = v
                
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id, values in delete_values.items():
            try:
                sample = Sample.objects.get(pk=object_id)
                delete_values[object_id]['sample_obj'] = sample
                pool = Pool.objects.get(name=values["pool_name"])
                delete_values[object_id]['pool_obj'] = pool

            except ObjectDoesNotExist as e:
                return JsonResponse({"error": str(e)})
        json_response = {"data": []}
        # Update database
        for obj_id, vals in delete_values.items():
            sample = vals['sample_obj']
            pool = vals['pool_obj']
            pool.samples.remove(sample)
            pool.save()
            
        return JsonResponse(json_response)

@login_required
def pooladdpools_table_update_view(request):
        # verify that the post is a remove action
    if (request.method == "POST") and (request.POST.get('action') == 'remove'):
        delete_values = {}
        # pull values from request
        for k, v in request.POST.items():
            if "data" in k:
                row_id = int(k.replace("[", " ").replace("]", "").split(" ")[1])
                if row_id not in delete_values:
                    delete_values[row_id] = {}
                if "pool_name" in k:
                    delete_values[row_id]['pool_name'] = v
                
        # Pull objects and check if object exists
        # return if object/s don't exist without doing any update
        for object_id, values in delete_values.items():
            try:
                pool_child = Pool.objects.get(pk=object_id)
                delete_values[object_id]['pool_child_obj'] = pool_child
                pool = Pool.objects.get(name=values["pool_name"])
                delete_values[object_id]['pool_obj'] = pool

            except ObjectDoesNotExist as e:
                return JsonResponse({"error": str(e)})
        json_response = {"data": []}
        # Update database
        for obj_id, vals in delete_values.items():
            pool_child = vals['pool_child_obj']
            pool = vals['pool_obj']
            pool.pools.remove(pool_child)
            pool.save()
            
        return JsonResponse(json_response)



@login_required
def giftcard_drawing_view(request):
    if request.method == 'POST':
        subject_data = {}
        email_list = []
        for event, sample_sz in zip(request.POST.getlist('event_id'), request.POST.getlist('sample_size')):
            subjects = list(np.random.choice(
                Event.objects.get(pk=event).subjects_with_collected_samples,
                int(sample_sz),
                replace=False))
            subject_list = Subject.objects.filter(id__in=subjects)
            email_list += [email for email in 
                list(Subject.objects.filter(id__in=subjects).values_list('email', flat=True))
                if email]
            subject_data.update({"{0}_{1}".format(event, v.id): {
                'subject': v, 'event': Event.objects.get(pk=event)
            } for v in subject_list})
        return render(
            request, 'lims/subject_giftcard_drawing_list.html',
            {'subject_data': subject_data, 'email_list': ";".join(email_list)})
    
    event_query_set = Event.objects.filter(
            date__lte=datetime.datetime.now().date()).order_by('-week', 'name')
    return render(request, 'lims/event_giftcard_list.html', {'event_list': event_query_set})


class SubjectGoogleFormsLink(SubjectPermissionsMixin, ListView):
    template_name = "lims/google_form_links.html"
    model = Subject
    context_object_name = 'subject_list'

    def get_queryset(self):
        None
        

@login_required
def google_form_json_view(request):
    try:
        subjects = []
        for subject in Subject.objects.filter(consent_status="Consented"):
            values = {k: v for k, v in subject.__dict__.items() if k in [
                'subject_ui', 'first_name', 'last_name', 'consent_status',
                'gardian_name', 'grade', 'email', 'phone']}
            values['location__name'] = subject.location.name
            values['phone'] = str(values['phone'])
            values['token'] = hashlib.sha1(subject.subject_ui.encode("utf-8")).hexdigest()
            link = "https://docs.google.com/forms/d/e/1FAIpQLSd36HGXLXU53GePdrhZYE3FRh-qC7OeHsYygBwHqLgQsKfGfg/viewform?usp=pp_url"
            link = link + "&entry.1867617705={fn}".format(fn=subject.first_name)
            link = link + "&entry.238338737={ln}".format(ln=subject.last_name)
            if subject.sex:
                link = link + "&entry.1104308818={sex}".format(sex=subject.sex.lower().capitalize())
            for race in subject.race.all():
                link = link + "&entry.1352371561={race}".format(race=race.name.replace(" ", "+"))
            if subject.ethnicity:
                link = link + "&entry.203578053=Yes"
            elif subject.ethnicity == False:
                link = link + "&entry.203578053=No"
            if subject.dose_1:
                link = link + "&entry.2056866576=Yes"
            elif subject.dose_1 == False:
                link = link + "&entry.2056866576=No"
            link = link + "&entry.697248355={month}".format(month=subject.dose_1_month)
            link = link + "&entry.549125450={year}".format(year=subject.dose_1_year)
            if subject.dose_2:
                link = link + "&entry.1053334543=Yes"
            elif subject.dose_2 == False:
                link = link + "&entry.1053334543=No"
            link = link + "&entry.2054062263={month}".format(month=subject.dose_2_month)
            link = link + "&entry.1851397949={year}".format(year=subject.dose_2_year)
            if subject.booster:
                link = link + "&entry.2133936943=Yes"
            elif subject.booster == False:
                link = link + "&entry.2133936943=No"
            link = link + "&entry.1233957808={month}".format(month=subject.booster_month)
            link = link + "&entry.77692500={year}".format(year=subject.booster_year)
            link = link + "&entry.2062908165={month}".format(month=subject.first_covid_case_month)
            link = link + "&entry.757052800={year}".format(year=subject.first_covid_case_year)
            link = link + "&entry.1598313138={month}".format(month=subject.second_covid_case_month)
            link = link + "&entry.285308076={year}".format(year=subject.second_covid_case_year)
            link = link + "&entry.762937797={month}".format(month=subject.third_covid_case_month)
            link = link + "&entry.310013965={year}".format(year=subject.third_covid_case_year)
            link = link + "&entry.1070433804={month}".format(month=subject.fourth_covid_case_month)
            link = link + "&entry.925635335={year}".format(year=subject.fourth_covid_case_year)
            link = link + "&entry.1824724562={month}".format(month=subject.fifth_covid_case_month)
            link = link + "&entry.281374859={year}".format(year=subject.fifth_covid_case_year)
            link = link + "&entry.1931846165={token}".format(token=values['token'])
            values['link'] = link
            subjects.append(values)
        data = {'data': subjects}
        return JsonResponse(data)
    except Exception as e:
        print(e)
        return JsonResponse({'data': [], 'error': str(e)})
