# Generated by Django 4.0.6 on 2024-03-06 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='empresa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('cnpj', models.CharField(max_length=18, unique=True)),
                ('telefone', models.CharField(max_length=15, unique=True)),
                ('telefone_whatsapp', models.CharField(max_length=15, null=True, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('endereco', models.CharField(max_length=255)),
            ],
        ),
    ]