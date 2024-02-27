from django.urls import path

from client import views

urlpatterns = [
    path('', views.personal_account_client, name='personalaccountclient'),
    path('calc_ins_auto/', views.calc_ins_auto, name='calc_ins_auto'),
    path('profile/', views.profile, name='profile'),
    path('agent_profile/', views.agent_profile, name='agent_profile'),
    path('calc_ins_health/', views.calc_ins_health, name='calc_ins_health'),
    path('select-date/', views.select_date, name='select_date'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('add_appointment_health/', views.add_appointment_health, name='add_appointment_health'),
    path('client_requests_car/', views.client_requests_car, name='client_requests_car'),
    path('client_requests_health/', views.client_requests_health, name='client_requests_health'),
    path('edit_appointment_car/<int:appointment_id>/', views.edit_appointment_car, name='edit_appointment_car'),
    path('health_contracts/', views.health_contracts, name='health_contracts'),
    path('car_contracts/', views.car_contracts, name='car_contracts'),
    path('appeal_car/', views.appeal_car, name='appeal_car'),
    path('appointment_car/<int:appointment_id>/delete/', views.delete_appointment_car, name='delete_appointment_car'),
    path('edit_appointment_health/<int:appointment_health_id>/', views.edit_appointment_health,
         name='edit_appointment_health'),
    path('delete_appointment_health/<int:appointment_health_id>/', views.delete_appointment_health,
         name='delete_appointment_health'),
    path('personalaccountemployee/', views.personal_account_employee, name='personalaccountemployee'),
    path('agent_requests_car/', views.agent_requests_car, name='agent_requests_car'),
    path('agent_requests_health/', views.agent_requests_health, name='agent_requests_health'),
    path('agent_requests_car_contract/', views.agent_requests_car_contract, name='agent_requests_car_contract'),
    path('agent_requests_health_contract/', views.agent_requests_health_contract, name='agent_requests_health_contract'),
    path('create-contract-car/<int:appointment_id>/', views.create_contract_car, name='create-contract-car'),
    path('create_contract_health/<int:appointment_id>/', views.create_contract_health, name='create_contract_health'),
]
