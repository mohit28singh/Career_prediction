# Generated by Django 3.1.1 on 2023-05-15 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0006_auto_20230514_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='pdf_files/')),
            ],
        ),
        migrations.DeleteModel(
            name='PDFDocument',
        ),
    ]
