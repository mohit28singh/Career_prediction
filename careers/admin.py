from django.contrib import admin
from .models import PDFDocument, ContactMessage
admin.site.register(PDFDocument)
admin.site.register(ContactMessage)
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'message')
    search_fields = ('email',)

admin.site.register(Feedback, FeedbackAdmin)