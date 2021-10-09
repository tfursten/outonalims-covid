from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Sample, Project, Location, Researcher
from .forms import ProjectForm, LocationForm, ResearcherForm

# Create your views here.

def index(request):
    return render(request, 'lims/dashboard.html')


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
    # fields = ['investigator', 'start_date', 'end_date', 'description', 'notes']
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
    # fields = ['investigator', 'start_date', 'end_date', 'description', 'notes']
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
