# Generated by Django 3.2.6 on 2021-09-07 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0016_auto_20210907_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='archivo',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='imagen',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
