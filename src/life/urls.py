from django.urls import path

from src.life import views

app_name = 'life'
urlpatterns = [
    path('life_insurance/', views.life_insurance_view, name='life_insurance_view'),

    path('agent_requests_health/', views.agent_requests_health, name='agent_requests_health'),

    path('create_life_insurance_record/', views.create_life_insurance_record, name='create_life_insurance_record'),

    path('user_life_insurance_requests/', views.user_life_insurance_requests, name='user_life_insurance_requests'),

    path('search_request_life_insurance/', views.search_request_life_insurance, name='search_request_life_insurance'),

    path('search_request_life_insurance_agent/', views.search_request_life_insurance_agent,
         name='search_request_life_insurance_agent'),

    path('life/contracts/', views.client_life_insurance_contracts, name='client_life_contracts'),

    path('life/claims/', views.client_life_claims, name='client_life_claims'),

    path('agent/create_life_insurance_record_agent/', views.create_life_insurance_record_agent,
         name='create_life_insurance_record_agent'),

    path('edit_life_record/<int:record_id>/', views.edit_life_record, name='edit_life_record'),

    path('edit_life_record/agent/<int:record_id>/', views.edit_life_record_agent, name='edit_life_record_agent'),

    path('agent_edit_life_record/<int:record_id>/', views.agent_edit_life_record, name='agent_edit_life_record'),

    path('delete_life_record/<int:record_id>/', views.delete_life_record, name='delete_life_record'),

    path('schedule-life-insurance-appointment/<int:record_id>/', views.schedule_life_insurance_appointment,
         name='schedule_life_insurance_appointment'),

    path('create-life-claim/<int:contract_id>/', views.create_life_claim, name='create_life_claim'),

    path('edit-life-claim/<int:claim_id>/', views.edit_life_claim, name='edit_life_claim'),

    path('choose-health-claim-schedule/<int:claim_id>/', views.choose_health_claim_schedule,
         name='choose_health_claim_schedule'),

    path('generate_pdf/<int:contract_id>', views.generate_pdf, name='generate_pdf'),

    path('agent/change-status/<int:record_id>/', views.change_status_to_in_progress,
         name='change_status_to_in_progress'),

    path('life/agent/contracts/', views.agent_life_contracts, name='agent_life_contracts'),

    path('create_life_contract/<int:record_id>/', views.create_life_contract, name='create_life_contract'),

]
