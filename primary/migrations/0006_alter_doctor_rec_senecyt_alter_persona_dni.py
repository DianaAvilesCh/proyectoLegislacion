# Generated by Django 5.0.1 on 2024-03-13 05:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("primary", "0005_alter_doctor_id_usuario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="rec_senecyt",
            field=models.CharField(max_length=17),
        ),
        migrations.AlterField(
            model_name="persona",
            name="dni",
            field=models.CharField(max_length=11),
        ),
    ]
