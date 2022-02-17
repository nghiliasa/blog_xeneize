from django.contrib import admin
from .models import Visit

# Register your models here.

class VisitAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'last_updated')
    list_display = ('username', 'created')
    list_filter = ('location',)
    search_fields = ('username',)
    ordering = ('created',)
    fieldsets = (
        (None, {'fields': (
            'username', 
            'computername', 
            'ip', 
            'country', 
            'city',
            'location',
            'zip',
            'lat',
            'lon',
            'created',
            'last_updated',
            )}),
    )

admin.site.register(Visit, VisitAdmin)
