# Generated by Django 3.2.6 on 2021-09-07 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0015_alter_comentario_archivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='comentarios',
        ),
        migrations.AddField(
            model_name='comentario',
            name='publicacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sitio.publicacion'),
            preserve_default=False,
        ),
    ]
