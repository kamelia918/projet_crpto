# Generated by Django 5.1.4 on 2025-03-23 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_alter_appointment_id_alter_doctor_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='name',
            new_name='username',
        ),
    ]
