from django.contrib import admin

from src.casco.models import Brand, CarModel, CascoRecord, CascoContract, \
    CascoPayoutAssessment, CascoClaim, CascoClaimAssessment

admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(CascoRecord)
admin.site.register(CascoContract)
admin.site.register(CascoPayoutAssessment)
admin.site.register(CascoClaim)
admin.site.register(CascoClaimAssessment)
