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
    path('delete_home_record/<int:record_id>/', views.delete_home_record, name='delete_home_record'),
    path('home-insurance-requests/', views.user_home_insurance_requests, name='home-insurance-requests'),
    path('schedule-appointment/<int:record_id>/', views.schedule_appointment, name='schedule-appointment'),
]
