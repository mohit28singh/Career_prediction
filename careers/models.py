from django.db import models

class PDFDocument(models.Model):
    Name = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/')
    
    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email