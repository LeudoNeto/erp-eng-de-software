from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets

from .produtos.models import produto
from .movimentacoes.models import transacao, produto_transacao

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your views here.
class DashboardViewSet(viewsets.ViewSet):

    def list(self, request):
        produtos = produto.objects.filter(empresa = request.user.empresa)
        vendas_totais = 0
        produtos_vendas = {k: 0 for k in produtos}
        for produto_transacao_obj in produto_transacao.objects.filter(tipo = "s", transacao__tipo = 'v',  transacao__empresa = request.user.empresa):
            produtos_vendas[produto_transacao_obj.produto] += produto_transacao_obj.quantidade
            vendas_totais += produto_transacao_obj.quantidade

        produtos_vendas = dict(sorted(produtos_vendas.items(), key=lambda item: item[1], reverse=True)[:4])

        vendas_totais_dos_quatro = sum(produtos_vendas.values())

        produtos_dashboard_data = {
            "vendas_totais": vendas_totais,
            "vendas_totais_dos_quatro": vendas_totais_dos_quatro,
            "produtos_mais_vendidos": [
                {
                    "produto": produto_obj.nome,
                    "foto": produto_obj.foto.url if produto_obj.foto else None,
                    "descricao": produto_obj.descricao,
                    "quantidade": quantidade
                } for produto_obj, quantidade in produtos_vendas.items()
            ],
        }

        # pegar os 8 últimos meses
        meses = []
        anos = []
        for i in range(8):
            data_relativa = datetime.now() - relativedelta(months=i)
            meses.insert(0, data_relativa.strftime("%B"))
            anos.insert(0, data_relativa.year)

        faturamento_dashboard_data = {
            "faturamento_ultimo_mes": sum(transacao.objects.filter(
                    empresa=request.user.empresa,
                    tipo__in=['v', 'p'],
                    data__month=datetime.now().month,
                    data__year=datetime.now().year
                ).values_list("valor_total_recebido", flat=True)),
            "faturamento": {
                mes[:3].title(): sum(transacao.objects.filter(
                    empresa=request.user.empresa,
                    tipo__in=['v', 'p'],
                    data__month=datetime.strptime(mes, "%B").month,
                    data__year=ano
                ).values_list("valor_total_recebido", flat=True)) for mes,ano in zip(meses, anos)
            },
            "despesas_ultimo_mes": sum(transacao.objects.filter(
                    empresa=request.user.empresa,
                    tipo__in=['c', 'r'],
                    data__month=datetime.now().month,
                    data__year=datetime.now().year
                ).values_list("valor_total_pago", flat=True)),
            "despesas": {
                mes[:3].title(): sum(transacao.objects.filter(
                    empresa=request.user.empresa,
                    tipo__in=['c', 'r'],
                    data__month=datetime.strptime(mes, "%B").month,
                    data__year=ano
                ).values_list("valor_total_pago", flat=True)) for mes,ano in zip(meses, anos)
            },
            "lucro_ultimo_mes": sum(transacao.objects.filter(
                    empresa=request.user.empresa,
                    tipo__in=['v', 'p'],
                    data__month=datetime.now().month,
                    data__year=datetime.now().year
                ).values_list("lucro", flat=True)),
            "lucro": {
                mes[:3].title(): sum(transacao.objects.filter(
                    empresa=request.user.empresa,
                    tipo__in=['v', 'p'],
                    data__month=datetime.strptime(mes, "%B").month,
                    data__year=ano
                ).values_list("lucro", flat=True)) for mes,ano in zip(meses, anos)
            }
        }

        faturamento_ultimo_mes = sum(transacao.objects.filter(
            empresa=request.user.empresa,
            tipo__in=['v', 'p'],
            data__month=datetime.now().month-1 if datetime.now().month > 1 else 12,
            data__year=datetime.now().year
        ).values_list("valor_total_recebido", flat=True))
        faturamento_dashboard_data['aumento_faturamento'] = (faturamento_dashboard_data['faturamento_ultimo_mes'] - faturamento_ultimo_mes) / faturamento_ultimo_mes if faturamento_ultimo_mes else 0

        despesas_ultimo_mes = sum(transacao.objects.filter(
            empresa=request.user.empresa,
            tipo__in=['c', 'r'],
            data__month=datetime.now().month-1 if datetime.now().month > 1 else 12,
            data__year=datetime.now().year
        ).values_list("valor_total_pago", flat=True))
        faturamento_dashboard_data['aumento_despesas'] = (faturamento_dashboard_data['despesas_ultimo_mes'] - despesas_ultimo_mes) / despesas_ultimo_mes if despesas_ultimo_mes else 0
        
        lucro_ultimo_mes = sum(transacao.objects.filter(
            empresa=request.user.empresa,
            tipo__in=['v', 'p'],
            data__month=datetime.now().month-1 if datetime.now().month > 1 else 12,
            data__year=datetime.now().year
        ).values_list("lucro", flat=True))
        faturamento_dashboard_data['aumento_lucro'] = (faturamento_dashboard_data['lucro_ultimo_mes'] - lucro_ultimo_mes) / lucro_ultimo_mes if lucro_ultimo_mes else 0

        return Response({
            "produtos_dashboard_data":produtos_dashboard_data,
            "faturamento_dashboard_data":faturamento_dashboard_data

        }, status=status.HTTP_200_OK)