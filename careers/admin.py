from django.contrib import admin
from .models import PDFFile

class PDFFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']
    search_fields = ['name']
    
admin.site.register(PDFFile, PDFFileAdmin)
