from django.contrib import admin

from src.property.models import HomeInsuranceRecord, HomeInsuranceContract, HomePayoutAssessment, HomeInsuranceClaim, \
    HomeClaimAssessment

admin.site.register(HomeInsuranceRecord)
admin.site.register(HomeInsuranceContract)
admin.site.register(HomePayoutAssessment)
admin.site.register(HomeInsuranceClaim)
admin.site.register(HomeClaimAssessment)
