document.addEventListener("DOMContentLoaded", function() {
    var modal_cadastro_troca = document.querySelector("#modal_cadastro_troca");
    var form_cadastro_troca = document.querySelector("#form_cadastro_troca");
    var salvar_troca = modal_cadastro_troca.querySelector("#salvar_troca");

    var excluir_troca_buttons = document.querySelectorAll("#excluir_troca");

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_troca.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        let produtos_transacao = [];
        let linhas_produtos_vendidos = document.querySelectorAll('.produto_vendido_cadastro');
        for (let linha_produto of linhas_produtos_vendidos) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                produtos_transacao.push({
                    'produto': linha_produto.querySelector('input[type=checkbox]').dataset.id,
                    'valor_custo': linha_produto.querySelector('#valor_custo').value.replace(/\D/g, '')/100,
                    'valor_venda': linha_produto.querySelector('#valor_venda').value.replace(/\D/g, '')/100,
                    'quantidade': linha_produto.querySelector('#quantidade').value,
                    'tipo': 's'
                })
            }
        }

        let linhas_produtos_comprados = document.querySelectorAll('.produto_comprado_cadastro');
        for (let linha_produto of linhas_produtos_comprados) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                produtos_transacao.push({
                    'produto': linha_produto.querySelector('input[type=checkbox]').dataset.id,
                    'valor_custo': linha_produto.querySelector('#valor_custo').value.replace(/\D/g, '')/100,
                    'valor_venda': linha_produto.querySelector('#valor_venda').value.replace(/\D/g, '')/100,
                    'quantidade': linha_produto.querySelector('#quantidade').value,
                    'tipo': 'e'
                })
            }
        }

        if (form_cadastro_troca.checkValidity() && produtos_transacao.length) {
            swal.fire({
                title: "Troca validada com sucesso!",
                text: "Clique em 'Confirmar' para salvar a troca.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let valor_de_venda_dos_produtos = modal_cadastro_troca.querySelector("#valor_produtos_vendidos").value.replace(/\D/g, '')/100;
                let valor_de_custo_dos_produtos = modal_cadastro_troca.querySelector("#valor_produtos_comprados").value.replace(/\D/g, '')/100;
                let valor_total_recebido = valor_de_venda_dos_produtos;
                let valor_total_pago = valor_de_custo_dos_produtos;
                let tipo = 't';

                let movimentacao = {
                    valor_total_recebido,
                    valor_total_pago,
                    valor_de_venda_dos_produtos,
                    valor_de_custo_dos_produtos,
                    tipo
                };

                movimentacao["calcular_lucro"] = modal_cadastro_troca.querySelector('#calcular_lucro').checked;

                let formData = new FormData(form_cadastro_troca);
                formData.append("transacao", JSON.stringify(movimentacao));
                formData.append("produtos_transacao", JSON.stringify(produtos_transacao));

                if (result.isConfirmed) {
                    fetch("/api/trocas/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Troca salva com sucesso!",
                                icon: "success"
                            }).then(() => {
                                window.location.reload();
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
                }
            });
        } else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                text: "Selecione os produtos envolvidos na troca.",
                icon: "error",
            })
        }
    });

    excluir_troca_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let troca_id = button.getAttribute('data-id');
            swal.fire({
                title: "Tem certeza que deseja excluir a movimentação?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch("/api/movimentacoes/" + troca_id, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf_token,
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Movimentação excluída com sucesso!",
                                icon: "success"
                            }).then(() => {
                                button.closest('tr').remove();
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
                    });
                }
            });
        });
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
    let valor_custo = linha_produto.querySelector('#valor_custo');
    let valor_venda = linha_produto.querySelector('#valor_venda');
    let valor_total_custo = linha_produto.querySelector('#valor_total_custo');
    let valor_total_venda = linha_produto.querySelector('#valor_total_venda');

    checkbox_produto.checked = (quantidade > 0) ? true : false;
    valor_total_custo.value = (quantidade * parseFloat(valor_custo.value.replace(/\D/g, ''))/100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
    valor_total_venda.value = (quantidade * parseFloat(valor_venda.value.replace(/\D/g, ''))/100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorCusto(input) {
    let linha_produto = input.closest('tr');

    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_custo = input.value;
    let valor_total_custo = linha_produto.querySelector('#valor_total_custo');

    valor_total_custo.value = (quantidade.value * parseFloat(valor_custo.replace(/\D/g, ''))/100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorVenda(input) {
    let linha_produto = input.closest('tr');
    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_venda = input.value;
    let valor_total_venda = linha_produto.querySelector('#valor_total_venda');

    valor_total_venda.value = (quantidade.value * parseFloat(valor_venda.replace(/\D/g, ''))/100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorTotalCusto(input) {
    let linha_produto = input.closest('tr');
    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_custo = linha_produto.querySelector('#valor_custo');
    let valor_total_custo = input.value;

    valor_custo.value = (parseFloat(valor_total_custo.replace(/\D/g, '')) / 100 / quantidade.value).toFixed(2).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorTotalVenda(input) {
    let linha_produto = input.closest('tr');
    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_venda = linha_produto.querySelector('#valor_venda');
    let valor_total_venda = input.value;

    valor_venda.value = (parseFloat(valor_total_venda.replace(/\D/g, '')) / 100 / quantidade.value).toFixed(2).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function atualizarValorProdutosVendidos(editar=false) {
    if (!editar) {  // cadastro
        let linhas_produto = document.querySelectorAll('.produto_vendido_cadastro');
        let valor_produtos_vendidos = 0;

        for (let linha_produto of linhas_produto) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                let valor_total_venda = linha_produto.querySelector('#valor_total_venda');
                valor_produtos_vendidos += parseFloat(valor_total_venda.value.replace(/\D/g, '')/100);
            }
        }

        modal_cadastro_troca.querySelector('#valor_produtos_vendidos').value = valor_produtos_vendidos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
}

function atualizarValorProdutosComprados(editar=false) {
    if (!editar) {  // cadastro
        let linhas_produto = document.querySelectorAll('.produto_comprado_cadastro');
        let valor_produtos_comprados = 0;

        for (let linha_produto of linhas_produto) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                let valor_total_custo = linha_produto.querySelector('#valor_total_custo');
                valor_produtos_comprados += parseFloat(valor_total_custo.value.replace(/\D/g, '')/100);
            }
        }

        modal_cadastro_troca.querySelector('#valor_produtos_comprados').value = valor_produtos_comprados.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
}