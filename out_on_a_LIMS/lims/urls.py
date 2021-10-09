from django.urls import path

from . import views

app_name = 'lims'

urlpatterns = [
    path('', views.index, name='index'),
    path('samples/', views.SampleListView.as_view(), name='sample_list'),
    path('samples/detail/<str:pk>/', views.SampleDetailView.as_view(), name="sample_detail"),
    # path('samples/detail/<str:sample_id>/edit/', views.edit_sample, name="edit_sample"),
    # path('samples/add/', views.add_sample, name="new_sample"),
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

]