# Generated by Django 3.1.1 on 2023-05-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0004_auto_20230514_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfdocument',
            name='document',
            field=models.FileField(upload_to='pdfs/'),
        ),
    ]
