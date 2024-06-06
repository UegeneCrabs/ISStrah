from django.urls import path

from src.osago import views

app_name = 'osago'
urlpatterns = [
    path('car/', views.car_view, name='car_view'),

    path('load-models/', views.load_models, name='load_models'),

    path('load-years/', views.load_years, name='load_years'),

    path('load-horsepowers/', views.load_horsepowers, name='load_horsepowers'),

    path('create_osago_record/', views.create_osago_record, name='create_osago_record'),

    path('client_osago_requests/', views.client_osago_requests, name='client_osago_requests'),

    path('search_request_osago/', views.search_request_osago, name='search_request_osago'),

    path('osago/contracts/', views.client_osago_contracts, name='client_osago_contracts'),

    path('osago/claims/', views.client_osago_claims, name='client_osago_claims'),

    path('edit_osago_record/<int:record_id>/', views.edit_osago_record, name='edit_osago_record'),

    path('delete_osago_record/<int:record_id>/', views.delete_osago_record, name='delete_osago_record'),

    path('schedule-osago-appointment/<int:record_id>/', views.schedule_osago_appointment,
         name='schedule_osago_appointment'),

    path('create-osago-claim/<int:contract_id>/', views.create_osago_claim, name='create_osago_claim'),

    path('edit-osago-claim/<int:claim_id>/', views.edit_osago_claim, name='edit_osago_claim'),

    path('choose-osago-claim-schedule/<int:claim_id>/', views.choose_osago_claim_schedule,
         name='choose_osago_claim_schedule'),

    path('generate_pdf/<int:contract_id>', views.generate_pdf, name='generate_pdf'),

    path('search_request_osago_insurance_agent/', views.search_request_osago_insurance_agent,
         name='search_request_osago_insurance_agent'),

    path('agent/change-status/<int:record_id>/', views.change_status_to_in_progress_casco,
         name='change_status_to_in_progress_casco'),

    path('agent_edit_osago_record/<int:record_id>/', views.agent_edit_osago_record, name='agent_edit_osago_record'),

    path('agent_requests_osago/', views.agent_requests_osago, name='agent_requests_osago'),

    path('delete_osago_record_agent/<int:record_id>/', views.delete_osago_record_agent,
         name='delete_osago_record_agent'),

    path('osago/agent/contracts/', views.agent_osago_contracts, name='agent_osago_contracts'),

    path('create_osago_contract/<int:record_id>/', views.create_osago_contract, name='create_osago_contract'),
]
