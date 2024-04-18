document.addEventListener("DOMContentLoaded", function() {
    var modal_emitir_nota_fiscal = document.querySelector("#modal_emitir_nota_fiscal");
    var form_emitir_nota_fiscal = document.querySelector("#form_emitir_nota_fiscal");
    var botao_emitir_nota_fiscal = modal_emitir_nota_fiscal.querySelector("#botao_emitir_nota_fiscal");

    botao_emitir_nota_fiscal.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_emitir_nota_fiscal.checkValidity()) {
            swal.fire({
                title: "Nota Fiscal validada com sucesso!",
                text: "Clique em 'Confirmar' para emitir a nota fiscal.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let icms_total = 0
                let produtos_nota_fiscal = [];
                let linhas_produtos_produtos_nota_fiscal = document.querySelectorAll('.produto_vendido_emitir');
                for (let linha_produto of linhas_produtos_produtos_nota_fiscal) {
                    if (linha_produto.querySelector('input[type=checkbox]').checked) {
                        let aliquota_icms = linha_produto.querySelector('input[type=checkbox]').dataset.icms / 100;
                        let valor_total = linha_produto.querySelector('#valor_total').value.replace(/\D/g, '')/100;
                        icms_total += valor_total * aliquota_icms;
                        produtos_nota_fiscal.push({
                            'produto': linha_produto.querySelector('input[type=checkbox]').dataset.id,
                            'valor_unitario': linha_produto.querySelector('#valor_unitario').value.replace(/\D/g, '')/100,
                            'valor_total': valor_total,
                            'quantidade': linha_produto.querySelector('#quantidade').value,
                            'valor_icms': (valor_total * aliquota_icms).toFixed(2),
                            'valor_total_liquido' : (valor_total - (valor_total * aliquota_icms)).toFixed(2)
                        })
                    }
                }

                let formData = new FormData(form_emitir_nota_fiscal);

                let valor_total_produtos = form_emitir_nota_fiscal.querySelector('#valor_total_produtos').value.replace(/\D/g, '')/100;
                let desconto = form_emitir_nota_fiscal.querySelector('#desconto').value.replace(/\D/g, '')/100;
                let taxas = form_emitir_nota_fiscal.querySelector('#taxas').value.replace(/\D/g, '')/100;

                formData.append("tipo", produtos_nota_fiscal.length ? "v" : "p");
                formData.append("valor_total_produtos", valor_total_produtos);
                formData.append("desconto", desconto);
                formData.append("taxas", taxas);
                formData.append("icms_total", icms_total.toFixed(2));
                formData.append("total", valor_total_produtos + taxas - desconto);
                formData.append("total_liquido", (valor_total_produtos + taxas - desconto - icms_total).toFixed(2));

                formData.append("produtos_nota_fiscal", JSON.stringify(produtos_nota_fiscal));

                if (result.isConfirmed) {
                    fetch("/api/notas_fiscais/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Nota fiscal emitida com sucesso!",
                                text: "Deseja imprimir a nota fiscal?",
                                icon: "success",
                                showCancelButton: true,
                                confirmButtonText: "Imprimir",
                                cancelButtonText: "Fechar"
                            })
                            .then(res => {
                                if (res.isConfirmed) {
                                    return response.json().then(data => {
                                        window.open("/financeiro/notas_fiscais/"+data.nota_fiscal, "_blank");
                                        window.location.reload();
                                    })
                                }
                                window.location.reload();
                            })
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
                }
            });
        } else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error",
            })
        }
    });

});

function formatarMoeda(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, '');
    valor = (valor / 100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
    input.value = valor;
}

function calcularPelaQuantidade(input) {
    let linha_produto = input.closest('tr');
    let checkbox_produto = linha_produto.querySelector('#checkbox_produto');
    let quantidade = input.value;
    let valor_unitario = linha_produto.querySelector('#valor_unitario');
    let valor_total = linha_produto.querySelector('#valor_total');

    checkbox_produto.checked = (quantidade > 0) ? true : false;
    valor_total.value = (quantidade * parseFloat(valor_unitario.value.replace(/\D/g, ''))/100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorVenda(input) {
    let linha_produto = input.closest('tr');
    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_unitario = input.value;
    let valor_total = linha_produto.querySelector('#valor_total');

    valor_total.value = (quantidade.value * parseFloat(valor_unitario.replace(/\D/g, ''))/100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorTotalVenda(input) {
    let linha_produto = input.closest('tr');
    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_unitario = linha_produto.querySelector('#valor_unitario');
    let valor_total = input.value;

    valor_unitario.value = (parseFloat(valor_total.replace(/\D/g, '')) / 100 / quantidade.value).toFixed(2).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function atualizarValorSubtotal(editar=false) {
    if (!editar) {  // cadastro
        let linhas_produto = document.querySelectorAll('.produto_vendido_emitir');
        let valor_produtos_vendidos = 0;

        for (let linha_produto of linhas_produto) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                let valor_total = linha_produto.querySelector('#valor_total');
                valor_produtos_vendidos += parseFloat(valor_total.value.replace(/\D/g, '')/100);
            }
        }

        modal_emitir_nota_fiscal.querySelector('#valor_total_produtos').value = valor_produtos_vendidos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
}
