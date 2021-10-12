from django.urls import path

from . import views

app_name = 'lims'

urlpatterns = [
    path('', views.index, name='index'),
    path('samples/', views.SampleListView.as_view(), name='sample_list'),
    path('samples/detail/<str:sample_id>/', views.SampleDetailView.as_view(), name="sample_detail"),
    # path('samples/print_labels/', views.print_sample_labels, name="print_sample_labels"),
    # path('samples/detail/<str:sample_id>/edit/', views.edit_sample, name="edit_sample"),
    path('samples/add/', views.add_samples, name="new_samples"),
    path('samples/add/<str:event_id>/', views.verify_subjects, name="verify_new_samples"),
    path('samples/event/<str:event_id>/', views.event_samples, name="event_samples"),
    path('samples/event/<str:event_id>/sample_label_pdf/', views.sample_labels_pdf, name="sample_label_pdf"),
    path('samples/choose_event/', views.select_event_for_sample, name="select_sample_event"),
    path('projects/', views.ProjectListView.as_view(), name="project_list"),
    path('projects/detail/<str:pk>/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('projects/detail/<str:pk>/edit/', views.ProjectUpdateView.as_view(), name="edit_project"),
    path('projects/new/', views.ProjectFormView.as_view(), name="new_project"),
    path('project/detail/<str:pk>/remove/', views.ProjectDeleteView.as_view(), name="delete_project"),
    path('locations/', views.LocationListView.as_view(), name="location_list"),
    path('locations/new/', views.LocationFormView.as_view(), name="new_location"),
    path('locations/detail/<str:pk>/', views.LocationDetailView.as_view(), name="location_detail"),
    path('locations/detail/<str:pk>/edit/', views.LocationUpdateView.as_view(), name="edit_location"),
    path('locations/detail/<str:pk>/remove/', views.LocationDeleteView.as_view(), name="delete_location"),
    path('researchers/', views.ResearcherListView.as_view(), name="researcher_list"),
    path('researchers/new/', views.ResearcherFormView.as_view(), name="new_researcher"),
    path('researchers/detail/<str:pk>/', views.ResearcherDetailView.as_view(), name="researcher_detail"),
    path('researchers/detail/<str:pk>/edit/', views.ResearcherUpdateView.as_view(), name="edit_researcher"),
    path('researchers/detail/<str:pk>/remove/', views.ResearcherDeleteView.as_view(), name="delete_researcher"),
    path('subject/', views.SubjectListView.as_view(), name="subject_list"),
    path('subject/new/', views.SubjectFormView.as_view(), name="new_subject"),
    path('subject/detail/<str:pk>/', views.SubjectDetailView.as_view(), name="subject_detail"),
    path('subject/detail/<str:pk>/edit/', views.SubjectUpdateView.as_view(), name="edit_subject"),
    path('subject/detail/<str:pk>/remove/', views.SubjectDeleteView.as_view(), name="delete_subject"),
    path('event/', views.EventListView.as_view(), name="event_list"),
    path('event/new/', views.EventFormView.as_view(), name="new_event"),
    path('event/detail/<str:pk>/', views.EventDetailView.as_view(), name="event_detail"),
    path('event/detail/<str:pk>/edit/', views.EventUpdateView.as_view(), name="edit_event"),
    path('event/detail/<str:pk>/remove/', views.EventDeleteView.as_view(), name="delete_event"),
    path('help/', views.help, name="help")
]