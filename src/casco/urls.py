from django.urls import path
from src.casco import views

app_name = 'casco'
urlpatterns = [
    path('car_casco/', views.car_view_casco, name='car_view_casco'),
    path('load_models/', views.load_models, name='load_models'),
    path('load_years/', views.load_years, name='load_years'),
    path('load_horsepowers/', views.load_horsepowers, name='load_horsepowers'),
    path('create_casco_record/', views.create_casco_record, name='create_casco_record'),
    path('client_casco_requests/', views.client_casco_requests, name='client_casco_requests'),
    path('search_request_casco/', views.search_request_casco, name='search_request_casco'),
    path('casco/contracts/', views.client_casco_contracts, name='client_casco_contracts'),
    path('casco/claims/', views.client_casco_claims, name='client_casco_claims'),
    path('edit_casco_record/<int:record_id>/', views.edit_casco_record, name='edit_casco_record'),
    path('delete_casco_record/<int:record_id>/', views.delete_casco_record, name='delete_casco_record'),
    path('schedule-casco-appointment/<int:record_id>/', views.schedule_casco_appointment,
         name='schedule_casco_appointment'),
    path('create-casco-claim/<int:contract_id>/', views.create_casco_claim, name='create_casco_claim'),
    path('edit-casco-claim/<int:claim_id>/', views.edit_casco_claim, name='edit_casco_claim'),
    path('choose-appraiser-schedule/<int:claim_id>/', views.choose_appraiser_schedule,
         name='choose_appraiser_schedule'),
    path('generate_pdf/<int:contract_id>', views.generate_pdf, name='generate_pdf'),
    path('agent_casco_requests/', views.agent_casco_requests, name='agent_casco_requests'),

    path('create_casco_contract/<int:casco_record_id>/', views.create_casco_contract, name='create_casco_contract'),
    path('casco/agent/contracts/', views.agent_casco_contracts, name='agent_casco_contracts'),

]
