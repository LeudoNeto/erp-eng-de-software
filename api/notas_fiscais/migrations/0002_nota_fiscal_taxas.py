# Generated by Django 4.0.6 on 2024-04-17 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas_fiscais', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nota_fiscal',
            name='taxas',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
