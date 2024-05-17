from django.contrib import admin

from src.osago.models import OsagoRecord, OsagoContract, \
    OsagoAutoPayoutAssessment, OsagoLifePayoutAssessment, OsagoClaim, OsagoClaimAutoAssessment, OsagoClaimLifeAssessment

admin.site.register(OsagoRecord)
admin.site.register(OsagoContract)
admin.site.register(OsagoAutoPayoutAssessment)
admin.site.register(OsagoLifePayoutAssessment)
admin.site.register(OsagoClaim)
admin.site.register(OsagoClaimAutoAssessment)
admin.site.register(OsagoClaimLifeAssessment)
