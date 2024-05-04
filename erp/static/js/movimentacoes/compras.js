document.addEventListener("DOMContentLoaded", function() {
    var modal_cadastro_compra = document.querySelector("#modal_cadastro_compra");
    var form_cadastro_compra = document.querySelector("#form_cadastro_compra");
    var salvar_compra = modal_cadastro_compra.querySelector("#salvar_compra");

    var editar_compra_buttons = document.querySelectorAll("#editar_compra");
    var modal_editar_compra = document.querySelector("#modal_editar_compra");
    var form_editar_compra = document.querySelector("#form_editar_compra");
    var salvar_editar_compra = modal_editar_compra.querySelector("#salvar_compra");

    var excluir_compra_buttons = document.querySelectorAll("#excluir_compra")

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_compra.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_cadastro_compra.checkValidity()) {
            swal.fire({
                title: "Compra validada com sucesso!",
                text: "Clique em 'Confirmar' para salvar a compra.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let cliente = modal_cadastro_compra.querySelector("#cliente").value;
                let metodo_pagamento = modal_cadastro_compra.querySelector("#metodo_pagamento").value;
                let valor_de_venda_dos_produtos = modal_cadastro_compra.querySelector("#valor_de_venda_dos_produtos").value.replace(/\D/g, '')/100;
                let valor_de_custo_dos_produtos = modal_cadastro_compra.querySelector("#subtotal").value.replace(/\D/g, '')/100;
                let taxas = modal_cadastro_compra.querySelector("#taxas").value.replace(/\D/g, '')/100;
                let desconto = modal_cadastro_compra.querySelector("#desconto").value.replace(/\D/g, '')/100;
                let valor_total_pago = (valor_de_custo_dos_produtos + taxas - desconto).toFixed(2);
                let valor_total_recebido = valor_de_venda_dos_produtos;

                if (valor_total_pago < 0) {
                    swal.fire({
                        title: "Erro",
                        text: "O valor total pago não pode ser negativo.",
                        icon: "error"
                    });
                    return;
                }

                let tipo;
                let produtos_transacao = [];
                let linhas_produtos = document.querySelectorAll('.produto_cadastro');
                for (let linha_produto of linhas_produtos) {
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

                tipo = produtos_transacao.length ? 'c' : 'r';

                let movimentacao = {
                    cliente,
                    valor_total_recebido,
                    valor_total_pago,
                    valor_de_venda_dos_produtos,
                    valor_de_custo_dos_produtos,
                    tipo,
                    taxas,
                    desconto,
                    metodo_pagamento
                };

                movimentacao["adicionar_estoque"] = modal_cadastro_compra.querySelector('#adicionar_estoque').checked;
                
                let formData = new FormData(form_cadastro_compra);
                formData.append("transacao", JSON.stringify(movimentacao));
                formData.append("produtos_transacao", JSON.stringify(produtos_transacao));

                if (result.isConfirmed) {
                    fetch("/api/compras/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Compra salva com sucesso!",
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
                icon: "error",
            })
        }
    });

    editar_compra_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let movimentacao_id = button.getAttribute('data-id');
            fetch(`/api/compras/${movimentacao_id}/`, {
                method: "GET"
            })
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        modal_editar_compra.querySelector("#cliente").value = data.cliente;
                        modal_editar_compra.querySelector("#metodo_pagamento").value = data.metodo_pagamento;
                        modal_editar_compra.querySelector("#valor_de_venda_dos_produtos").value = data.valor_de_venda_dos_produtos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        modal_editar_compra.querySelector("#subtotal").value = data.valor_de_custo_dos_produtos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        modal_editar_compra.querySelector("#taxas").value = data.taxas.toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        modal_editar_compra.querySelector("#desconto").value = data.desconto.toLocaleString('pt-BR', {minimumFractionDigits: 2});

                        for (let produto_transacao of data.produtos_transacao) {
                            let linha_produto = document.querySelector(`.produto_editar [data-id="${produto_transacao.produto}"]`).closest('tr');
                            linha_produto.querySelector('#checkbox_produto').checked = true;
                            linha_produto.querySelector('#quantidade').value = produto_transacao.quantidade;
                            linha_produto.querySelector('#valor_custo').value = (produto_transacao.valor_custo).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                            linha_produto.querySelector('#valor_venda').value = (produto_transacao.valor_venda).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                            linha_produto.querySelector('#valor_total_custo').value = ((produto_transacao.valor_custo * produto_transacao.quantidade)).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                            linha_produto.querySelector('#valor_total_venda').value = ((produto_transacao.valor_venda * produto_transacao.quantidade)).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        }

                        salvar_editar_compra.dataset.id = movimentacao_id;
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
        });
    });

    salvar_editar_compra.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_editar_compra.checkValidity()) {
            swal.fire({
                title: "Compra validada com sucesso!",
                text: "Clique em 'Confirmar' para salvar a compra.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let cliente = modal_editar_compra.querySelector("#cliente").value;
                let metodo_pagamento = modal_editar_compra.querySelector("#metodo_pagamento").value;
                let valor_de_venda_dos_produtos = modal_editar_compra.querySelector("#valor_de_venda_dos_produtos").value.replace(/\D/g, '')/100;
                let valor_de_custo_dos_produtos = modal_editar_compra.querySelector("#subtotal").value.replace(/\D/g, '')/100;
                let taxas = modal_editar_compra.querySelector("#taxas").value.replace(/\D/g, '')/100;
                let desconto = modal_editar_compra.querySelector("#desconto").value.replace(/\D/g, '')/100;
                let valor_total_pago = (valor_de_custo_dos_produtos + taxas - desconto).toFixed(2);
                let valor_total_recebido = valor_de_venda_dos_produtos;

                if (valor_total_pago < 0) {
                    swal.fire({
                        title: "Erro",
                        text: "O valor total pago não pode ser negativo.",
                        icon: "error"
                    });
                    return;
                }

                let tipo;
                let produtos_transacao = [];
                let linhas_produtos = document.querySelectorAll('.produto_editar');
                for (let linha_produto of linhas_produtos) {
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

                tipo = produtos_transacao.length ? 'c' : 'r';

                let movimentacao = {
                    cliente,
                    valor_total_recebido,
                    valor_total_pago,
                    valor_de_venda_dos_produtos,
                    valor_de_custo_dos_produtos,
                    tipo,
                    taxas,
                    desconto,
                    metodo_pagamento
                };

                let movimentacao_id = salvar_editar_compra.dataset.id;
                let formData = new FormData(form_editar_compra);
                formData.append("transacao", JSON.stringify(movimentacao));
                formData.append("produtos_transacao", JSON.stringify(produtos_transacao));

                if (result.isConfirmed) {
                    fetch(`/api/compras/${movimentacao_id}/`, {
                        method: "PUT",
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Compra salva com sucesso!",
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
                icon: "error",
            })
        }
    });

    excluir_compra_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let movimentacao_id = button.getAttribute('data-id');
            swal.fire({
                title: "Tem certeza que deseja excluir a compra?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/api/movimentacoes/${movimentacao_id}/`, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf_token
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Compra excluída com sucesso!",
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

    valor_custo.value = (parseFloat(valor_total_custo.replace(/\D/g, '')) / 100 / quantidade.value).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function calcularPeloValorTotalVenda(input) {
    let linha_produto = input.closest('tr');
    let quantidade = linha_produto.querySelector('#quantidade');
    let valor_venda = linha_produto.querySelector('#valor_venda');
    let valor_total_venda = input.value;

    valor_venda.value = (parseFloat(valor_total_venda.replace(/\D/g, '')) / 100 / quantidade.value).toLocaleString('pt-BR', {minimumFractionDigits: 2});
}

function atualizarValorSubtotal(editar=false) {
    if (!editar) {  // cadastro
        let linhas_produto = document.querySelectorAll('.produto_cadastro');
        let valor_de_venda_dos_produtos = 0;
        let subtotal = 0;

        for (let linha_produto of linhas_produto) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                let valor_custo_total = linha_produto.querySelector('#valor_total_custo');
                let valor_venda_total = linha_produto.querySelector('#valor_total_venda');
                valor_de_venda_dos_produtos += parseFloat(valor_venda_total.value.replace(/\D/g, '')/100);
                subtotal += parseFloat(valor_custo_total.value.replace(/\D/g, '')/100);
            }
        }

        modal_cadastro_compra.querySelector('#subtotal').value = subtotal.toLocaleString('pt-BR', {minimumFractionDigits: 2});
        modal_cadastro_compra.querySelector('#valor_de_venda_dos_produtos').value = valor_de_venda_dos_produtos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
    else {
        let linhas_produto = document.querySelectorAll('.produto_editar');
        let valor_de_venda_dos_produtos = 0;
        let subtotal = 0;

        for (let linha_produto of linhas_produto) {
            let valor_custo_total = linha_produto.querySelector('#valor_total_custo');
            let valor_venda_total = linha_produto.querySelector('#valor_total_venda');
            valor_de_venda_dos_produtos += parseFloat(valor_venda_total.value.replace(/\D/g, '')/100);
            subtotal += parseFloat(valor_custo_total.value.replace(/\D/g, '')/100);
        }

        modal_editar_compra.querySelector('#subtotal').value = subtotal.toLocaleString('pt-BR', {minimumFractionDigits: 2});
        modal_editar_compra.querySelector('#valor_de_venda_dos_produtos').value = valor_de_venda_dos_produtos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
}
