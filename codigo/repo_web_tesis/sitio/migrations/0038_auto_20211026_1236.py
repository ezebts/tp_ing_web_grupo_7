# Generated by Django 3.2.8 on 2021-10-26 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0037_comentario_responde'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_lectura', models.DateField(null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='seguimiento',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='u_seguidores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seguimiento',
            name='usuario_siguiendo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='u_siguiendo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='NotificacionNuevoSeguidor',
            fields=[
                ('notificacion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sitio.notificacion')),
                ('seguimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitio.comentario')),
            ],
            bases=('sitio.notificacion',),
        ),
        migrations.CreateModel(
            name='NotificacionNuevoComentario',
            fields=[
                ('notificacion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sitio.notificacion')),
                ('comentario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitio.comentario')),
            ],
            bases=('sitio.notificacion',),
        ),
        migrations.CreateModel(
            name='NotificacionNuevaPublicacion',
            fields=[
                ('notificacion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sitio.notificacion')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitio.publicacion')),
            ],
            bases=('sitio.notificacion',),
        ),
    ]
