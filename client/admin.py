from django.contrib import admin

from client.models import Availability, AppointmentsCar, AppointmentsHealth, PaymentTableHealth, ContractHealth, \
    ContractCar, PaymentTableCar

admin.site.register(Availability)
admin.site.register(AppointmentsCar)
admin.site.register(AppointmentsHealth)
admin.site.register(PaymentTableHealth)
admin.site.register(ContractHealth)
admin.site.register(ContractCar)
admin.site.register(PaymentTableCar)
