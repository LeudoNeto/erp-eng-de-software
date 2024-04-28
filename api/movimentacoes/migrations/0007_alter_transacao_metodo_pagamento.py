# Generated by Django 4.0.6 on 2024-04-24 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacoes', '0006_alter_transacao_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='metodo_pagamento',
            field=models.CharField(choices=[('d', 'Dinheiro'), ('p', 'PIX'), ('d', 'Débito'), ('c', 'Crédito')], max_length=1, null=True),
        ),
    ]
