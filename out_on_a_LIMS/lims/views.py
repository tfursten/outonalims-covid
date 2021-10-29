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
    Sample, Project, Location, Researcher, Event, Subject, Box, Pool)
from .forms import (
    ProjectForm, LocationForm, ResearcherForm,
    EventForm, SubjectForm, SampleForm, BoxForm,
    SelectEventForm, SamplePrint, PoolForm, PoolUpdateForm,
    FixIDS)
from cualid import create_ids
import reportlab
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab_qrcode import QRCodeImage
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from difflib import get_close_matches
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
    
    success_message = "Subject was successfully added"

    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))


class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject


class SubjectUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Subject
    template_name_suffix = '_update'
    form_class = SubjectForm
    success_message = "Subject was successfully updated"
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
        n = len(subjects['not_created'])
        size = 6
        # TODO limit unique ids to a project
        existing_ids =[sample.name for sample in Sample.objects.all()]
        cual_ids = [cid[0] for cid in create_ids(n, size, existing_ids=existing_ids)]
        for cual_id, subject in zip(cual_ids, subjects['not_created']):
            # create new samples for subjects that have
            # not been added.
            sample = Sample(name = cual_id, subject=subject, 
                collection_event=event, location=subject.location)
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


def sample_label_options(request, event_id):
    form = SamplePrint()
    if request.method == "POST":
        form = SamplePrint(request.POST)
        if form.is_valid():
            start_position = request.POST.get('start_position')
            label_paper = request.POST.get('label_paper')
            reps = request.POST.get('replicates')
            sort_by1 = request.POST.get('sort_by1')
            sort_by2 = request.POST.get('sort_by2')
            sort_by3 = request.POST.get('sort_by3')

            return redirect('lims:sample_label_pdf',
                event_id=event_id, start_position=start_position,
                label_paper=label_paper, replicates=reps,
                sort_by1=sort_by1, sort_by2=sort_by2, sort_by3=sort_by3)
    return render(request, 'lims/sample_print_options.html', {'form': form})    





def get_x_y_coordinates(columns, rows, x_start, y_start):
    x = 44.5 + 7.87
    y = -12.7
    for column in range(columns):
        for row in range(rows):
            x_coord = x_start + (x*column)
            y_coord = y_start + (y*row)
            yield (x_coord*mm, y_coord*mm)

    


def sample_labels_pdf(
    request, event_id, start_position,
    label_paper, replicates, sort_by1,
    sort_by2, sort_by3):
    """
    Use Cual-id code to generate labels with barcodes
    """
    # Create a file-like buffer to receive PDF data.

    event = Event.objects.get(pk=event_id)
    samples = Sample.get_samples_for_event(event, sort_by1, sort_by2, sort_by3)
    ids = [sample.name for sample in samples]
    locations = [str(sample.subject.location) for sample in samples]
    grades = [str(sample.subject.grade) for sample in samples]
    last_names = [str(sample.subject.last_name) for sample in samples]
    first_names = [str(sample.subject.first_name) for sample in samples]


    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    barcode_canvas = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter 
    print(page_width * mm, page_height * mm)
    columns=4
    rows=20
    x_start=7
    y_start=265
    xy_coords = list(get_x_y_coordinates(columns, rows, x_start, y_start))


    c = int(start_position) - 1
    for (id_, ln, fn, loc, grade) in zip(ids, last_names, first_names, locations, grades):
        for rep in range(int(replicates)):
            x = xy_coords[c][0] + (1.5 * mm)
            y = xy_coords[c][1] - (1.3 * mm)
            qr_size = 13
            qr_code = QRCodeImage(id_, size=qr_size * mm)
            qr_code.drawOn(barcode_canvas, x , y - ((qr_size - 4) * mm))
            # barcode = code128.Code128(id_, barWidth=0.19*mm,
            #                               barHeight=11*mm)
            # barcode.drawOn(barcode_canvas, x, y)
        
            barcode_canvas.setFont("Helvetica", 7)
            barcode_canvas.drawString(x + (qr_size * mm), y, "{0}".format(id_))
            barcode_canvas.drawString(x + (qr_size * mm), (y - (2.3 * mm)), "{0},{1}".format(ln[:15], fn[:15]))
            barcode_canvas.drawString(x + (qr_size * mm), (y - (4.6 * mm)), "{0} Grade: {1}".format(event.name[:25], grade))
            barcode_canvas.drawString(x + (qr_size * mm), (y - (6.9 * mm)), "{0}".format(loc)[:25])
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
        filename='{}_sample_labels.pdf'.format(event.name.replace(" ", "_")))


class SampleDetailView(LoginRequiredMixin, DetailView):
    model = Sample

class SampleUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Sample
    template_name_suffix = '_update'
    form_class = SampleForm
    success_message = "Sample was successfully updated"
    def get_success_url(self):
        return reverse('lims:sample_detail', args=(self.object.id,))
    


# ============== BOXES ================================
class BoxListView(LoginRequiredMixin, ListView):
    template_name_suffix = "_list"
    context_object_name = 'box_list'

    def get_queryset(self):
        """
        Return all boxes
        """
        return Box.objects.all()

class BoxFormView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Box
    template_name_suffix = '_new'
    form_class = BoxForm
    success_message = "Storage box was successfully added: %(box_name)s"

    def get_success_url(self):
        return reverse('lims:box_detail', args=(self.object.id,))


class BoxDetailView(LoginRequiredMixin, DetailView):
    model = Box


class BoxUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Box
    template_name_suffix = '_update'
    form_class = BoxForm
    success_message = "Box was successfully updated:  %(box_name)s"
    def get_success_url(self):
        return reverse('lims:box_detail', args=(self.object.id,))

class BoxDeleteView(LoginRequiredMixin, DeleteView):
    model = Box
    success_url = reverse_lazy('lims:box_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")


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
        context['sample_list']=Sample.objects.all()
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
        pools = Pool.objects.exclude(id__in=[pool_id])
        context['pool_list'] = pools
        return context
        
    def post(self, request, *args, **kwargs):
        pool = self.get_object()
        print(request.POST.getlist('ids'))
        pools = [Pool.objects.get(pk=int(p)) for p in request.POST.getlist('ids')]
        print(pools)
        for p in pools:
            pool.pools.add(p)
        pool.save()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('lims:pool_detail', args=(self.object.id,))


class PoolDetailView(LoginRequiredMixin, DetailView):
    model = Pool


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
