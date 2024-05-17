from django.contrib import admin

from src.life.models import LifeClaimAssessment, LifeInsuranceRecord, LifeInsuranceContract, HealthClaim, \
    LifePayoutAssessment

admin.site.register(LifeInsuranceRecord)
admin.site.register(LifeInsuranceContract)
admin.site.register(HealthClaim)
admin.site.register(LifePayoutAssessment)
admin.site.register(LifeClaimAssessment)
