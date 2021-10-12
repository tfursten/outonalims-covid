import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, CreateView, DeleteView, UpdateView, DetailView)
from django.contrib import messages
from django.db.models import ProtectedError
from .models import (
    Sample, Project, Location, Researcher, Event, Subject)
from .forms import (
    ProjectForm, LocationForm, ResearcherForm, EventForm, SubjectForm, SelectEventForm)
from cualid import create_ids
import reportlab
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
# Create your views here.

def index(request):
    return render(request, 'lims/dashboard.html')


# ============== PROJECTS ================================

class ProjectListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'project_list'

    def get_queryset(self):
        """
        Return all projects
        """
        return Project.objects.all()

class ProjectFormView(LoginRequiredMixin, SuccessMessageMixin,CreateView):
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

    def get_queryset(self):
        """
        Return all locations
        """
        return Location.objects.all()

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

    def get_queryset(self):
        """
        Return all locations
        """
        return Researcher.objects.all()

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

    def get_queryset(self):
        """
        Return all locations
        """
        return Event.objects.all()

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
class SubjectListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'subject_list'

    def get_queryset(self):
        """
        Return all locations
        """
        return Subject.objects.all()

class SubjectFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Subject
    template_name_suffix = '_new'
    form_class = SubjectForm
    success_message = "Subject was successfully added: %(subject_ui)s"

    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject


class SubjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Subject
    template_name_suffix = '_update'
    form_class = SubjectForm
    success_message = "Subject was successfully updated:  %(subject_ui)s"
    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('lims:subject_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")





# ============== SAMPLES ================================

class SampleListView(LoginRequiredMixin, ListView):
    template_name = "lims/sample_list.html"
    context_object_name = 'sample_list'

    def get_queryset(self):
        """
        Return all samples
        """
        return Sample.objects.all()

def add_samples(request):
    # TODO: add logic to mark an event as complete after collection date so that we don't add new samples
    form = SelectEventForm()
    if request.method == 'POST':
        form = SelectEventForm(request.POST)
        if form.is_valid():
            event = request.POST.get('event')
            return redirect('lims:verify_new_samples', event_id=event)
    return render(request, 'lims/samples_new.html', {'form':form})


def verify_subjects(request, event_id):
    event = Event.objects.get(pk=event_id)
    subjects = Sample.get_subjects_at_event(event)
    if request.method == "GET":
        return render(
            request, 'lims/verify_new_samples.html',
            {'created': subjects['created'],
            'not_created': subjects['not_created'],
            'event_name': event.name})
    elif request.method == "POST":
        print("POST")
        n = len(subjects['not_created'])
        size = 6
        # TODO limit unique ids to a project
        existing_ids =[sample.sample_id for sample in Sample.objects.all()]
        cual_ids = [cid[0] for cid in create_ids(n, size, existing_ids=existing_ids)]
        for cual_id, subject in zip(cual_ids, subjects['not_created']):
            # create new samples for subjects that have
            # not been added.
            sample = Sample(sample_id = cual_id, subject=subject, collection_event=event)
            sample.save(force_insert=True)
        return redirect('lims:event_samples', event_id=event_id)


def event_samples(request, event_id):
    event = Event.objects.get(pk=event_id)
    samples = Sample.get_samples_for_event(event)
    context = {'samples': samples, 'event': event}
    return render(request, 'lims/samples_for_event.html', context)
    


def select_event_for_sample(request):
    form = SelectEventForm()
    if request.method == "POST":
        form = SelectEventForm(request.POST)
        if form.is_valid():
            event = request.POST.get('event')
            return redirect('lims:event_samples', event_id=event)
    return render(request, 'lims/samples_print_labels.html', {'form': form})


def get_x_y_coordinates(columns, rows, x_start, y_start):
    x = 51.6
    y = -28.42
    for column in range(columns):
        for row in range(rows):
            x_coord = x_start + (x*column)
            y_coord = y_start + (y*row)
            yield (x_coord*mm, y_coord*mm)



def sample_labels_pdf(request, event_id):
    # Create a file-like buffer to receive PDF data.
    event = Event.objects.get(pk=event_id)
    samples = Sample.get_samples_for_event(event)
    ids = [sample.sample_id for sample in samples]
    first_names = [str(sample.subject.first_name) for sample in samples]
    last_names = [str(sample.subject.last_name) for sample in samples]
    subject_ids = [str(sample.subject.subject_ui) for sample in samples]
    print(last_names)
    columns=4
    rows=9
    x_start=1.9
    y_start=257.2
    xy_coords = list(get_x_y_coordinates(columns, rows, x_start, y_start))
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    barcode_canvas = canvas.Canvas(buffer)
    c = 0
    for (id_, fn, ln, sid) in zip(ids, first_names, last_names, subject_ids):
        x = xy_coords[c][0]
        y = xy_coords[c][1]
        barcode = code128.Code128(id_, barWidth=0.19*mm,
                                      barHeight=11*mm)
        barcode.drawOn(barcode_canvas, x, y)
        barcode_canvas.setFont("Helvetica", 8)
        barcode_canvas.drawString((x + 12 * mm), (y - 4 * mm), id_)
        barcode_canvas.drawString((x + 6 * mm), (y - 8 * mm), "{0}, {1}".format(ln, fn))
        if c < ((rows*columns) - 1):
            c += 1
        else:
            c = 0

    # Close the PDF object cleanly, and we're done.
    barcode_canvas.showPage()
    barcode_canvas.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True,
        filename='{}_sample_labels.pdf'.format(event.name.replace(" ", "_")))


class SampleDetailView(LoginRequiredMixin, DetailView):
    model = Sample
    

def help(request):
    return render(request, 'lims/help.html')
