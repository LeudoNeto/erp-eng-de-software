document.addEventListener("DOMContentLoaded", function() {
    var produtos_mais_vendidos_lista = document.querySelector("#produtos_mais_vendidos_lista");
    var vendas_totais_text = document.querySelector("#vendas_totais");
    var vendas_totais_dos_quatro_text = document.querySelector("#vendas_totais_dos_quatro");
    var faturamento_ultimo_mes_text = document.querySelector("#faturamento_ultimo_mes");
    var despesas_ultimo_mes_text = document.querySelector("#despesas_ultimo_mes");
    var lucro_ultimo_mes_text = document.querySelector("#lucro_ultimo_mes");

    fetch('/api/dashboard/')
    .then(response => {
        if (response.ok) {
            return response.json().then(data => {
                makeChartOrderStatistics(data.produtos_dashboard_data);
                for (let produto of data.produtos_dashboard_data.produtos_mais_vendidos) {
                    produtos_mais_vendidos_lista.innerHTML += makeProduto(produto);
                    vendas_totais_text.innerText = data.produtos_dashboard_data.vendas_totais;
                    vendas_totais_dos_quatro_text.innerText = data.produtos_dashboard_data.vendas_totais_dos_quatro;
                }
                makeIncomeChart("#incomeChartFaturamento", data.faturamento_dashboard_data.faturamento);
                makeIncomeChart("#incomeChartDespesas", data.faturamento_dashboard_data.despesas);
                makeIncomeChart("#incomeChartLucro", data.faturamento_dashboard_data.lucro);
                faturamento_ultimo_mes_text.innerText = "R$  " +  data.faturamento_dashboard_data.faturamento_ultimo_mes.toLocaleString('pt-BR', {minimumFractionDigits: 2});
                let aumento_faturamento = data.faturamento_dashboard_data.aumento_faturamento;
                faturamento_ultimo_mes_text.parentElement.innerHTML += `
                    <small class="text-${aumento_faturamento > 0 ? "success" : "danger"} fw-semibold">
                        <i class="bx bx-chevron-${aumento_faturamento > 0 ? "up" : "down"}"></i>
                        ${(Math.abs(aumento_faturamento) * 100).toFixed(1)}%
                    </small>
                `
                despesas_ultimo_mes_text.innerText = "R$  " + data.faturamento_dashboard_data.despesas_ultimo_mes.toLocaleString('pt-BR', {minimumFractionDigits: 2});
                let aumento_despesas = data.faturamento_dashboard_data.aumento_despesas;
                despesas_ultimo_mes_text.parentElement.innerHTML += `
                    <small class="text-${aumento_despesas > 0 ? "success" : "danger"} fw-semibold">
                        <i class="bx bx-chevron-${aumento_despesas > 0 ? "up" : "down"}"></i>
                        ${(Math.abs(aumento_despesas) * 100).toFixed(1)}%
                    </small>
                `
                lucro_ultimo_mes_text.innerText = "R$  " + data.faturamento_dashboard_data.lucro_ultimo_mes.toLocaleString('pt-BR', {minimumFractionDigits: 2});
                let aumento_lucro = data.faturamento_dashboard_data.aumento_lucro;
                lucro_ultimo_mes_text.parentElement.innerHTML += `
                    <small class="text-${aumento_lucro > 0 ? "success" : "danger"} fw-semibold">
                        <i class="bx bx-chevron-${aumento_lucro > 0 ? "up" : "down"}"></i>
                        ${(Math.abs(aumento_lucro) * 100).toFixed(1)}%
                    </small>
                `

            });
        }
        else {
            return response.json().then(data => {
                swal.fire({
                    title: data.erro,
                    text: data.detalhes,
                    icon: "error"
                });
            });
        }
        
    })
      

    if (document.documentElement.getAttribute('data-theme') == 'light') {
        var cardColor = config.colors.white;
        var headingColor = config.colors.headingColor;
        var axisColor = config.colors.axisColor;
        var borderColor = config.colors.borderColor;    
    }
    else {
        var cardColor = config.colors.dark;
        var headingColor = config.colors.white;
        var axisColor = config.colors.axisColor;
        var borderColor = config.colors.borderColor;
    }
    function makeChartOrderStatistics(data) {
        // Order Statistics Chart
        // --------------------------------------------------------------------
        const chartOrderStatistics = document.querySelector('#orderStatisticsChart'),
        
        orderChartConfig = {
            chart: {
                height: 165,
                width: 130,
                type: 'donut'
            },      
            labels: data.produtos_mais_vendidos.map(produto => produto.produto),
            series: data.produtos_mais_vendidos.map(produto => produto.quantidade),
            colors: [config.colors.primary, config.colors.secondary, config.colors.info, config.colors.success],
            stroke: {
                width: 5,
                colors: cardColor
            },
            dataLabels: {
            enabled: false,
            formatter: function (val, opt) {
                return parseInt(val) + '%';
            }
            },
            legend: {
            show: false
            },
            grid: {
            padding: {
                top: 0,
                bottom: 0,
                right: 15
            }
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '75%',
                        labels: {
                            show: true,
                            value: {
                                fontSize: '1.5rem',
                                fontFamily: 'Public Sans',
                                color: headingColor,
                                offsetY: -15,
                                formatter: function (val) {
                                    return parseInt((val*100)/data.vendas_totais_dos_quatro) + '%';
                                }
                            },
                            name: {
                            offsetY: 20,
                            fontFamily: 'Public Sans'
                            },
                            total: {
                                show: true,
                                fontSize: '0.8125rem',
                                color: config.colors.primary,
                                label: data.produtos_mais_vendidos[0].produto,
                                formatter: function (w) {
                                    return parseInt((data.produtos_mais_vendidos[0].quantidade*100)/data.vendas_totais_dos_quatro) + "%";
                                }
                            }
                        }
                    }
                }
            }
        };
        if (typeof chartOrderStatistics !== undefined && chartOrderStatistics !== null) {
        const statisticsChart = new ApexCharts(chartOrderStatistics, orderChartConfig);
        statisticsChart.render();
        }
    }
    
    function makeIncomeChart(chart_id, data) {
        console.log(data);
        // Income Chart - Area chart
        // --------------------------------------------------------------------
        const incomeChartEl = document.querySelector(chart_id),
        incomeChartConfig = {
            series: [
            {
                data: Object.values(data)
            }
            ],
            chart: {
            height: 215,
            parentHeightOffset: 0,
            parentWidthOffset: 0,
            toolbar: {
                show: false
            },
            type: 'area'
            },
            dataLabels: {
            enabled: false
            },
            stroke: {
            width: 2,
            curve: 'smooth'
            },
            legend: {
            show: false
            },
            markers: {
            size: 6,
            colors: 'transparent',
            strokeColors: 'transparent',
            strokeWidth: 4,
            discrete: [
                {
                fillColor: config.colors.white,
                seriesIndex: 0,
                dataPointIndex: 7,
                strokeColor: config.colors.primary,
                strokeWidth: 2,
                size: 6,
                radius: 8
                }
            ],
            hover: {
                size: 7
            }
            },
            colors: [config.colors.primary],
            fill: {
            type: 'gradient',
            gradient: {
                shade: cardColor,
                shadeIntensity: 0.6,
                opacityFrom: 0.5,
                opacityTo: 0.25,
                stops: [0, 95, 100]
            }
            },
            grid: {
            borderColor: borderColor,
            strokeDashArray: 3,
            padding: {
                top: -20,
                bottom: -8,
                left: -10,
                right: 8
            }
            },
            xaxis: {
            categories: Object.keys(data),
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            },
            labels: {
                show: true,
                style: {
                fontSize: '13px',
                colors: axisColor
                }
            }
            },
            yaxis: {
            labels: {
                show: false
            },
            min: Object.values(data).reduce((a, b) => Math.min(a, b)) * 0.9,
            max: Object.values(data).reduce((a, b) => Math.max(a, b)) * 1.1,
            tickAmount: 4
            }
        };
        if (typeof incomeChartEl !== undefined && incomeChartEl !== null) {
        const incomeChart = new ApexCharts(incomeChartEl, incomeChartConfig);
        incomeChart.render();
        }
    }
  
});

function makeProduto(produto) {
    let foto = produto.foto ? `<img src="${produto.foto}" />` : `<span class="avatar-initial rounded bg-label-primary"
                                                                    ><i class="bx bxs-component"></i
                                                                ></span>`;
    return `
    <li class="d-flex mb-4 pb-1">
        <div class="avatar flex-shrink-0 me-3">
            ${foto}
        </div>
        <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
        <div class="me-2">
            <h6 class="mb-0">${produto.produto}</h6>
            <small class="text-muted">${produto.descricao}</small>
        </div>
        <div class="user-progress">
            <small class="fw-semibold">${produto.quantidade}</small>
        </div>
        </div>
    </li>
    `;
}