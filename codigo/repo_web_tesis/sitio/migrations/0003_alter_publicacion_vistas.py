# Generated by Django 3.2.6 on 2021-08-31 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0002_autor_comentario_publicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='vistas',
            field=models.IntegerField(),
        ),
    ]