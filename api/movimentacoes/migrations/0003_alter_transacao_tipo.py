# Generated by Django 4.0.6 on 2024-03-06 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacoes', '0002_rename_valor_compra_produto_transacao_valor_custo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='tipo',
            field=models.CharField(choices=[('c', 'Compra'), ('v', 'Venda'), ('t', 'Troca'), ('p', 'Serviço Prestado'), ('r', 'Serviço Recebido')], max_length=1),
        ),
    ]
