# Generated by Django 3.2.8 on 2021-10-26 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0038_auto_20211026_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacionnuevoseguidor',
            name='seguimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sitio.seguimiento'),
        ),
    ]
