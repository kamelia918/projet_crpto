# from django.contrib import admin
# from .models import *

# admin.site.register(Doctor)
# admin.site.register(Patient)
# # admin.site.register(PatientProfile)
# admin.site.register(Hospital)
# admin.site.register(Appointment)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile , Patient

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Patient)



