# Generated by Django 4.0.6 on 2024-03-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='foto',
            field=models.FileField(null=True, upload_to='usuarios/'),
        ),
    ]