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
]
