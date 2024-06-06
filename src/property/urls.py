from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('home_insurance/', views.home_insurance_view, name='home_insurance_view'),

    path('create_home_insurance_record/', views.create_home_insurance_record, name='create_home_insurance_record'),

    path('user_home_insurance_requests/', views.user_home_insurance_requests, name='user_home_insurance_requests'),

    path('search_request_home_insurance/', views.search_request_home_insurance, name='search_request_home_insurance'),

    path('home_insurance/contracts/', views.client_home_insurance_contracts, name='client_home_insurance_contracts'),

    path('home_insurance/claims/', views.client_home_insurance_claims, name='client_home_insurance_claims'),

    path('edit_home_record/<int:record_id>/', views.edit_home_record, name='edit_home_record'),

    path('edit_home_record_agent/<int:record_id>/', views.edit_home_record_agent, name='edit_home_record_agent'),

    path('delete_home_record/<int:record_id>/', views.delete_home_record, name='delete_home_record'),

    path('home-insurance-requests/', views.user_home_insurance_requests, name='home-insurance-requests'),

    path('schedule-appointment/<int:record_id>/', views.schedule_appointment, name='schedule-appointment'),

    path('create-home-claim/<int:contract_id>/', views.create_home_claim, name='create_home_claim'),

    path('edit-home-claim/<int:claim_id>/', views.edit_home_claim, name='edit_home_claim'),

    path('choose-home-insurance-claim-schedule/<int:claim_id>/', views.choose_home_insurance_claim_schedule,
         name='choose_home_insurance_claim_schedule'),

    path('generate_pdf/<int:contract_id>', views.generate_pdf, name='generate_pdf'),

    path('agent_home_insurance_requests/', views.agent_home_insurance_requests, name='agent_home_insurance_requests'),

    path('agent/change-status-property/<int:record_id>/', views.change_status_property_to_in_progress,
         name='change_status_property_to_in_progress'),

    path('delete_home_record_agent/<int:record_id>/', views.delete_home_record_agent,
         name='delete_home_record_agent'),

    path('home_insurance/agent/contracts/', views.agent_home_insurance_contracts,
         name='agent_home_insurance_contracts'),

    path('create_home_insurance_contract/<int:record_id>/', views.create_home_insurance_contract,
         name='create_home_insurance_contract'),

]
