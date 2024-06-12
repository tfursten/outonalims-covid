from django.urls import path

from . import views

app_name = 'lims'

urlpatterns = [
    path('', views.index, name="index"),
    path('samples/', views.SampleListView.as_view(), name="sample_list"),
    path('samples/json/', views.sample_list_json_view, name="sample_list_json"),
    path('samples/search/', views.search_view, name="sample_search"),
    path('samples/detail/<str:pk>/', views.SampleDetailView.as_view(), name="sample_detail"),
    path('samples/detail/<str:pk>/result/new', views.SampleResultSampleFormView.as_view(), name="new_result_sample"),
    path('samples/detail/<str:pk>/edit/', views.SampleUpdateView.as_view(), name="edit_sample"),
    path('samples/event/<str:event_id>/', views.event_samples, name="event_samples"),
    path('samples/add/', views.add_samples, name="new_samples"),
    path('samples/add/<str:event_id>/<str:sample_type>', views.verify_subjects, name="verify_new_samples"),
    path('samples/event/<str:event_id>/sample-label-options/', views.sample_label_options, name="sample_labels_options"),
    path('samples/sample-storage-label-options/', views.sample_storage_label_options, name="sample_storage_labels_options"),
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
    path('subject/json/', views.subject_list_json_view, name="subject_list_json"),
    path('subject/detail_list', views.SubjectDetailListView.as_view(), name="subject_list_detail"),
    path('subject/new/', views.SubjectFormView.as_view(), name="new_subject"),
    path('subject/detail/<str:pk>/', views.SubjectDetailView.as_view(), name="subject_detail"),
    path('subject/detail/<str:pk>/edit/', views.SubjectUpdateView.as_view(), name="edit_subject"),
    path('subject/detail/<str:pk>/remove/', views.SubjectDeleteView.as_view(), name="delete_subject"),
    path('event/', views.EventListView.as_view(), name="event_list"),
    path('event/new/', views.EventFormView.as_view(), name="new_event"),
    path('event/detail/<str:pk>/', views.EventDetailView.as_view(), name="event_detail"),
    path('event/detail/<str:pk>/edit/', views.EventUpdateView.as_view(), name="edit_event"),
    path('event/detail/<str:pk>/remove/', views.EventDeleteView.as_view(), name="delete_event"),
    path('event/notices/', views.sample_notices, name="sample_notice"),
    path('event/detail/<str:event_id>/notice-text/', views.sample_notices, name="sample_notice_text"),
    path('event/<str:event_id>/notices/', views.sample_notices_pdf, name="sample_notice_pdf"),
    path('event/choose-event/', views.select_event_for_sample, name="select_sample_event"),
    path('event/list/choose-event/', views.select_event_for_sample_list, name="select_sample_event_list"),
    path('event/<str:event_id>/subject-list/', views.subject_list, name="subject_list"),
    path('sample-box/', views.SampleBoxListView.as_view(), name="sample_box_list"),
    path('sample-box/new/', views.SampleBoxFormView.as_view(), name="new_sample_box"),
    path('sample-box/detail/<str:pk>/', views.SampleBoxDetailView.as_view(), name="sample_box_detail"),
    path('sample-box/detail/<str:pk>/edit/', views.SampleBoxUpdateView.as_view(), name="edit_sample_box"),
    path('sample-box/detail/<str:pk>/remove/', views.SampleBoxDeleteView.as_view(), name="delete_sample_box"),
    path('sample-box/detail/<str:pk>/copy-samples/', views.SampleBoxCopySamples.as_view(), name="sample_box_copy_samples"),
    path('sample-box/detail/<str:pk>/upload-samples/', views.SampleBoxPositionUploadView.as_view(), name="sample_box_upload_samples"),
    path('sample-box/detail/<str:pk_box>/position/<str:pk>/', views.SampleBoxPosDetailView.as_view(), name="sample_box_position_detail"),
    path('sample-box/detail/<str:pk_box>/position/<str:pk>/edit-sample/', views.SampleBoxPositionUpdateView.as_view(), name="edit_sample_box_position"),
    path('sample-box/detail/<str:pk_box>/position/<str:pk>/add-samples/', views.SampleBoxPositionContinuousUpdateView.as_view(), name="edit_sample_box_position_continuous"),
    path('pool-box/', views.PoolBoxListView.as_view(), name="pool_box_list"),
    path('pool-box/new/', views.PoolBoxFormView.as_view(), name="new_pool_box"),
    path('pool-box/detail/<str:pk>/', views.PoolBoxDetailView.as_view(), name="pool_box_detail"),
    path('pool-box/detail/<str:pk>/edit/', views.PoolBoxUpdateView.as_view(), name="edit_pool_box"),
    path('pool-box/detail/<str:pk>/remove/', views.PoolBoxDeleteView.as_view(), name="delete_pool_box"),
    path('pool-box/detail/<str:pk_box>/position/<str:pk>/', views.PoolBoxPosDetailView.as_view(), name="pool_box_position_detail"),
    path('pool-box/detail/<str:pk_box>/position/<str:pk>/edit-pool/', views.PoolBoxPositionUpdateView.as_view(), name="edit_pool_box_position"),
    path('pool-box/detail/<str:pk_box>/position/<str:pk>/add-pools/', views.PoolBoxPositionContinuousUpdateView.as_view(), name="edit_pool_box_position_continuous"),
    path('pool/', views.PoolListView.as_view(), name="pool_list"),
    path('pool/new/', views.PoolFormView.as_view(), name="new_pool"),
    path('pool/detail/<str:pk>/add-samples', views.PoolAddSamples.as_view(), name="add_pool_samples"),
    path('pool/detail/<str:pk>/add-pools', views.PoolAddPools.as_view(), name="add_pool_pools"),
    path('pool/detail/<str:pk>/result/new', views.PoolResultSampleFormView.as_view(), name="new_result_pool"),
    path('pool/detail/<str:pk>/', views.PoolDetailView.as_view(), name="pool_detail"),
    path('pool/detail/<str:pk>/edit/', views.PoolUpdateView.as_view(), name="edit_pool"),
    path('pool/detail/<str:pk>/remove/', views.PoolDeleteView.as_view(), name="delete_pool"),
    path('pool/detail/<str:pk>/report/', views.PoolReportDetailView.as_view(), name="pool_report"),
    path('fix-ids/', views.fix_ids, name="fix_ids"),
    path('labels/', views.LabelListView.as_view(), name="label_list"),
    path('labels/new/', views.LabelFormView.as_view(), name="new_label"),
    path('labels/detail/<str:pk>/', views.LabelDetailView.as_view(), name="label_detail"),
    path('labels/detail/<str:pk>/edit/', views.LabelUpdateView.as_view(), name="edit_label"),
    path('labels/detail/<str:pk>/remove/', views.LabelDeleteView.as_view(), name="delete_label"),
    path('test/', views.TestListView.as_view(), name="test_list"),
    path('test/new/', views.TestFormView.as_view(), name="new_test"),
    path('test/detail/<str:pk>/', views.TestDetailView.as_view(), name="test_detail"),
    path('test/detail/<str:pk>/edit/', views.TestUpdateView.as_view(), name="edit_test"),
    path('test/detail/<str:pk>/remove/', views.TestDeleteView.as_view(), name="delete_test"),
    path('sequencing/', views.SequenceListView.as_view(), name="sequence_list"),
    path('sequencing/new/', views.SequenceFormView.as_view(), name="new_sequence"),
    path('sequencing/detail/<str:pk>/', views.SequenceDetailView.as_view(), name="sequence_detail"),
    path('sequencing/detail/<str:pk>/add-samples', views.SequenceAddSamples.as_view(), name="add_sequence_samples"),
    path('sequencing/detail/<str:pk>/add-pools', views.SequenceAddPools.as_view(), name="add_sequence_pools"),
    path('sequencing/detail/<str:pk>/edit/', views.SequenceUpdateView.as_view(), name="edit_sequence"),
    path('sequencing/detail/<str:pk>/remove/', views.SequenceDeleteView.as_view(), name="delete_sequence"),
    path('sequencing/sample-list/', views.sequenced_samples, name="sequenced_samples"),
    path('sequencing/data/', views.sequencing_endpoint, name='sequencing_endpoint'),
    path('sample-result/', views.SampleResultListView.as_view(), name="sample_result_list"),
    path('sample-result/new/', views.SampleResultFormView.as_view(), name="new_sample_result"),
    path('sample-result/upload/', views.upload_sample_result_file, name="upload_sample_result"),
    path('sample-result/add-multiple/', views.sampleresult_multiple_view, name="new_multi_sample_result"),
    path('sample-result/add-multiple/<str:test_id>/<str:rep>/add-samples/', views.sampleresult_multiple_add_samples, name="sampleresult_multiple_add_samples"),
    path('sample-result/detail/<str:pk>/', views.SampleResultDetailView.as_view(), name="sample_result_detail"),
    path('sample-result/detail/<str:pk>/edit/', views.SampleResultUpdateView.as_view(), name="edit_sample_result"),
    path('sample-result/detail/<str:pk>/remove/', views.SampleResultDeleteView.as_view(), name="delete_sample_result"),
    path('pool-result/', views.PoolResultListView.as_view(), name="pool_result_list"),
    path('pool-result/new/', views.PoolResultFormView.as_view(), name="new_pool_result"),
    path('pool-result/upload/', views.upload_pool_result_file, name="upload_pool_result"),
    path('pool-result/add-multiple/', views.poolresult_multiple_view, name="new_multi_pool_result"),
    path('pool-result/add-multiple/<str:test_id>/<str:rep>/add-pools/', views.poolresult_multiple_add_pools, name="poolresult_multiple_add_pools"),
    path('pool-result/detail/<str:pk>/', views.PoolResultDetailView.as_view(), name="pool_result_detail"),
    path('pool-result/detail/<str:pk>/edit/', views.PoolResultUpdateView.as_view(), name="edit_pool_result"),
    path('pool-result/detail/<str:pk>/remove/', views.PoolResultDeleteView.as_view(), name="delete_pool_result"),
    path('help/', views.help, name="help"),
    path('samples/table-edit/', views.sample_table_update_view, name="sample_table_update"),
    path('pools/table-edit/', views.pool_table_update_view, name="pool_table_update"),
    path('poolboxes/table-edit/', views.poolbox_table_update_view, name="poolbox_table_update"),
    path('sampleboxes/table-edit/', views.samplebox_table_update_view, name="samplebox_table_update"),
    path('sampleresults/table-edit/', views.sampleresults_table_update_view, name="sampleresults_table_update"),
    path('poolresults/table-edit/', views.poolresults_table_update_view, name="poolresults_table_update"),
    path('pooladdsamples/table-edit/', views.pooladdsamples_table_update_view, name="pooladdsamples_table_update"),
    path('pooladdpools/table-edit/', views.pooladdpools_table_update_view, name="pooladdpools_table_update"),
    path('events/table-edit/', views.events_table_update_view, name="events_table_update"),
    path('analysis/select/', views.select_analysis_view, name="select_analysis"),
    path('analysis/<str:project>/<str:test>/data/', views.analysis_data_view, name="analysis_data"),
    path('giftcards/', views.giftcard_drawing_view, name="giftcards"),
    path('subjects/google-form-links/', views.SubjectGoogleFormsLink.as_view(), name="google_form_links"),
    path('subjects/google-form-json/', views.google_form_json_view, name="google_form_list_json"),
    path('report/select/', views.select_report, name="report_data"),
    path('dashboard/', views.dashboard_report, name="dashboard_report"),
    path('dashboard/data/', views.dashboard_endpoint, name="dashboard_endpoint"),

]