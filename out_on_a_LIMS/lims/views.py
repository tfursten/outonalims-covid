from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from django.db.models import ProtectedError
from .models import (
    Sample, Project, Location, Researcher, Event, Subject)
from .forms import (
    ProjectForm, LocationForm, ResearcherForm, EventForm, SubjectForm)

# Create your views here.

def index(request):
    return render(request, 'lims/dashboard.html')


# ============== PROJECTS ================================

class ProjectListView(generic.ListView):
    template_name_suffix = "_list"
    context_object_name = 'project_list'

    def get_queryset(self):
        """
        Return all projects
        """
        return Project.objects.all()

class ProjectFormView(SuccessMessageMixin, generic.CreateView):
    model = Project
    template_name_suffix = '_new'
    form_class = ProjectForm
    success_message = "Project was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:project_detail', args=(self.object.id,))


class ProjectDetailView(generic.DetailView):
    model = Project

class ProjectUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    # fields = ['investigator', 'start_date', 'end_date', 'description', 'notes']
    template_name_suffix = '_update'
    form_class = ProjectForm
    success_message = "Project was successfully updated:  %(name)s"
    
    def get_success_url(self):
        return reverse('lims:project_detail', args=(self.object.id,))


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy('lims:project_list', args=())
    
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== LOCATIONS ================================

class LocationListView(generic.ListView):
    template_name_suffix = "_list"
    context_object_name = 'location_list'

    def get_queryset(self):
        """
        Return all locations
        """
        return Location.objects.all()

class LocationFormView(SuccessMessageMixin, generic.CreateView):
    model = Location
    template_name_suffix = '_new'
    form_class = LocationForm
    success_message = "Location was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:location_detail', args=(self.object.id,))


class LocationDetailView(generic.DetailView):
    model = Location

class LocationUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Location
    template_name_suffix = '_update'
    form_class = LocationForm
    success_message = "Location was successfully updated:  %(name)s"
    def get_success_url(self):
        return reverse('lims:location_detail', args=(self.object.id,))


class LocationDeleteView(generic.DeleteView):
    model = Location
    success_url = reverse_lazy('lims:location_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")


# ============== RESEARCHER ================================


class ResearcherListView(generic.ListView):
    template_name_suffix = "_list"
    context_object_name = 'researcher_list'

    def get_queryset(self):
        """
        Return all locations
        """
        return Researcher.objects.all()

class ResearcherFormView(SuccessMessageMixin, generic.CreateView):
    model = Researcher
    template_name_suffix = '_new'
    form_class = ResearcherForm
    success_message = "Researcher was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:researcher_detail', args=(self.object.id,))

class ResearcherDetailView(generic.DetailView):
    model = Researcher


class ResearcherUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Researcher
    template_name_suffix = '_update'
    form_class = ResearcherForm
    success_message = "Researcher was successfully updated:  %(name)s"
    def get_success_url(self):
        return reverse('lims:researcher_detail', args=(self.object.id,))


class ResearcherDeleteView(generic.DeleteView):
    model = Researcher
    success_url = reverse_lazy('lims:researcher_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== EVENTS ================================
class EventListView(generic.ListView):
    template_name_suffix = "_list"
    context_object_name = 'event_list'

    def get_queryset(self):
        """
        Return all locations
        """
        return Event.objects.all()

class EventFormView(SuccessMessageMixin, generic.CreateView):
    model = Event
    template_name_suffix = '_new'
    form_class = EventForm
    success_message = "Event was successfully added: %(name)s"

    def get_success_url(self):
        return reverse('lims:event_detail', args=(self.object.id,))


class EventDetailView(generic.DetailView):
    model = Event


class EventUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Event
    template_name_suffix = '_update'
    form_class = EventForm
    success_message = "Collection event was successfully updated:  %(name)s"
    def get_success_url(self):
        return reverse('lims:event_detail', args=(self.object.id,))

class EventDeleteView(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('lims:event_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")

# ============== SUBJECTS ================================
class SubjectListView(generic.ListView):
    template_name_suffix = "_list"
    context_object_name = 'subject_list'

    def get_queryset(self):
        """
        Return all locations
        """
        return Subject.objects.all()

class SubjectFormView(SuccessMessageMixin, generic.CreateView):
    model = Subject
    template_name_suffix = '_new'
    form_class = SubjectForm
    success_message = "Subject was successfully added: %(subject_ui)s"

    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))


class SubjectDetailView(generic.DetailView):
    model = Subject


class SubjectUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Subject
    template_name_suffix = '_update'
    form_class = SubjectForm
    success_message = "Subject was successfully updated:  %(subject_ui)s"
    def get_success_url(self):
        return reverse('lims:subject_detail', args=(self.object.id,))

class SubjectDeleteView(generic.DeleteView):
    model = Subject
    success_url = reverse_lazy('lims:subject_list', args=())
    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, "lims/protected_error.html")





# ============== SAMPLES ================================

class SampleListView(generic.ListView):
    template_name = "lims/sample_list.html"
    context_object_name = 'sample_list'

    def get_queryset(self):
        """
        Return all samples
        """
        return Sample.objects.all()


class SampleDetailView(generic.DetailView):
    model = Sample



    

def help(request):
    return render(request, 'lims/base.html')
