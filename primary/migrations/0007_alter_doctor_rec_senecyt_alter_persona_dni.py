# Generated by Django 5.0.1 on 2024-03-13 06:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("primary", "0006_alter_doctor_rec_senecyt_alter_persona_dni"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="rec_senecyt",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="persona",
            name="dni",
            field=models.CharField(max_length=10),
        ),
    ]
