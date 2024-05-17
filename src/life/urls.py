from django.urls import path

from src.life import views

app_name = 'life'
urlpatterns = [
    path('life_insurance/', views.life_insurance_view, name='life_insurance_view'),
    path('create_life_insurance_record/', views.create_life_insurance_record, name='create_life_insurance_record'),
    path('user_life_insurance_requests/', views.user_life_insurance_requests, name='user_life_insurance_requests'),
    path('search_request_life_insurance/', views.search_request_life_insurance, name='search_request_life_insurance'),
    path('life/contracts/', views.client_life_insurance_contracts, name='client_life_contracts'),
    path('life/claims/', views.client_life_claims, name='client_life_claims'),
    path('edit_life_record/<int:record_id>/', views.edit_life_record, name='edit_life_record'),
    path('delete_life_record/<int:record_id>/', views.delete_life_record, name='delete_life_record'),
    path('schedule-life-insurance-appointment/<int:record_id>/', views.schedule_life_insurance_appointment,
         name='schedule_life_insurance_appointment'),
]
