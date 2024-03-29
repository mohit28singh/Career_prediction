# Generated by Django 3.1.1 on 2023-05-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0007_auto_20230515_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
            ],
        ),
        migrations.DeleteModel(
            name='PDFFile',
        ),
    ]
