'''

from django.contrib import admin
from .models import TempParent, TempParentLearnerRelationship

@admin.register(TempParent)
class TempParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')

@admin.register(TempParentLearnerRelationship)
class TempParentLearnerRelationshipAdmin(admin.ModelAdmin):
    list_display = ('parent', 'learner_id', 'is_primary_contact')
'''
