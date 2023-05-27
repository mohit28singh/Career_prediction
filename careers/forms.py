from django import forms
from .models import PDFDocument

class PDFUploadForm(forms.ModelForm):
  class Meta:
        model = PDFDocument
        fields = ('Name', 'pdf_file')
        labels = {
            'pdf_file': '',
        }