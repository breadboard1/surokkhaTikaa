from django.contrib import admin
from . import models


class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',), }

class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',), }


admin.site.register(models.Specialization, SpecializationAdmin)
admin.site.register(models.Designation, DesignationAdmin)
admin.site.register(models.Doctor)