# Generated by Django 3.2.6 on 2021-09-01 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0004_remove_comentario_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='archivo',
            field=models.FileField(default=0, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='titulo',
            field=models.CharField(max_length=50),
        ),
    ]
