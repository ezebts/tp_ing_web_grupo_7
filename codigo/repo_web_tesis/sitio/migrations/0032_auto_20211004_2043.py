# Generated by Django 3.2.6 on 2021-10-04 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0031_auto_20210928_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seguimiento',
            old_name='usuario_id',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='seguimiento',
            old_name='usuario_siguiendo_id',
            new_name='usuario_siguiendo',
        ),
    ]