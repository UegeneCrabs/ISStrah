from django.contrib import admin

from src.users.models import AgentSchedule, AppraiserSchedule

admin.site.register(AgentSchedule)
admin.site.register(AppraiserSchedule)

