from django.db import models

class PDFDocument(models.Model):
    Name = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/')
