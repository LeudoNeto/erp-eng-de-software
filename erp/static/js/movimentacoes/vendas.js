document.addEventListener("DOMContentLoaded", function() {
    var modal_cadastro_venda = document.querySelector("#modal_cadastro_venda");
    var form_cadastro_venda = document.querySelector("#form_cadastro_venda");
    var salvar_venda = modal_cadastro_venda.querySelector("#salvar_venda");

    var editar_venda_buttons = document.querySelectorAll("#editar_venda");
    var modal_editar_venda = document.querySelector("#modal_editar_venda");
    var form_editar_venda = document.querySelector("#form_editar_venda");
    var salvar_editar_venda = modal_editar_venda.querySelector("#salvar_venda");

    var excluir_venda_buttons = document.querySelectorAll("#excluir_venda")

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_venda.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (!modal_cadastro_venda.querySelector("#cliente_endereco").value && modal_cadastro_venda.querySelector('#emitir_nota_fiscal').checked) {
            swal.fire({
                title: "Para emitir NF é necessário informar o endereço do cliente.",
                icon: "error"
            });
            return;
        }

        if (!modal_cadastro_venda.querySelector("#vendedor").value && modal_cadastro_venda.querySelector('#emitir_comprovante').checked) {
            swal.fire({
                title: "Para emitir comprovante é necessário informar o vendedor.",
                icon: "error"
            });
            return;
        }

        if (form_cadastro_venda.checkValidity()) {
            swal.fire({
                title: "Venda validada com sucesso!",
                text: "Clique em 'Confirmar' para salvar a venda.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let cliente = modal_cadastro_venda.querySelector("#cliente").value;
                let cliente_endereco = modal_cadastro_venda.querySelector("#cliente_endereco").value;
                let vendedor = modal_cadastro_venda.querySelector("#vendedor").value;
                let metodo_pagamento = modal_cadastro_venda.querySelector("#metodo_pagamento").value;
                let valor_de_venda_dos_produtos = modal_cadastro_venda.querySelector("#subtotal").value.replace(/\D/g, '')/100;
                let valor_de_custo_dos_produtos = modal_cadastro_venda.querySelector("#valor_de_custo_dos_produtos").value.replace(/\D/g, '')/100;
                let taxas = modal_cadastro_venda.querySelector("#taxas").value.replace(/\D/g, '')/100;
                let desconto = modal_cadastro_venda.querySelector("#desconto").value.replace(/\D/g, '')/100;
                let valor_total_pago = valor_de_custo_dos_produtos;
                let valor_total_recebido = (valor_de_venda_dos_produtos + taxas - desconto).toFixed(2);

                let tipo;
                let produtos_transacao = [];
                let linhas_produtos = document.querySelectorAll('.produto_cadastro, .produto_estoque_cadastro');
                for (let linha_produto of linhas_produtos) {
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

                let produtos_estoque = []
                if (modal_cadastro_venda.querySelector('#remover_estoque').checked) {                
                    let linhas_produtos_estoque = document.querySelectorAll('.produto_estoque_cadastro');
                    for (let produto_estoque of linhas_produtos_estoque) {
                        if (produto_estoque.querySelector('input[type=checkbox]').checked) {
                            if (produto_estoque.querySelector('#quantidade').value > produto_estoque.dataset.quantidade) {
                                swal.fire({
                                    title: "Quantidade do produto indisponível em estoque.",
                                    text: `Produto: ${produto_estoque.querySelector("#produto_estoque_nome")}`,
                                    icon: "error",
                                });
                                return;
                            }
                            produtos_estoque.push({
                                'id': produto_estoque.querySelector('input[type=checkbox]').dataset.produtoEstoqueId,
                                'quantidade': produto_estoque.querySelector('#quantidade').value,
                            })
                        }
                    }
                }

                tipo = produtos_transacao.length ? 'v' : 'p';

                let movimentacao = {
                    cliente,
                    cliente_endereco,
                    vendedor,
                    valor_total_recebido,
                    valor_total_pago,
                    valor_de_venda_dos_produtos,
                    valor_de_custo_dos_produtos,
                    tipo,
                    taxas,
                    desconto,
                    metodo_pagamento
                };

                movimentacao["remover_estoque"] = modal_cadastro_venda.querySelector('#remover_estoque').checked;
                movimentacao["emitir_comprovante"] = modal_cadastro_venda.querySelector('#emitir_comprovante').checked;
                movimentacao["emitir_nota_fiscal"] = modal_cadastro_venda.querySelector('#emitir_nota_fiscal').checked;
                
                let formData = new FormData(form_cadastro_venda);
                formData.append("transacao", JSON.stringify(movimentacao));
                formData.append("produtos_transacao", JSON.stringify(produtos_transacao));
                formData.append("produtos_estoque", JSON.stringify(produtos_estoque));

                if (result.isConfirmed) {
                    fetch("/api/vendas/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            if (movimentacao["emitir_comprovante"]) {
                                return response.json().then(data => {
                                    swal.fire({
                                        title: "Venda salva com sucesso!",
                                        text: "Emitindo comprovante...",
                                        icon: "info",
                                        showConfirmButton: false,
                                        allowOutsideClick: false
                                    })
                                    let venda_id = data.venda_id;
                                    fetch(`/api/vendas/${data.venda_id}/comprovante_da_venda/`, {
                                        headers: {
                                            "X-CSRFToken": csrf_token,
                                        },
                                        method: "POST"
                                    })
                                    .then(response => {
                                        if (response.ok) {
                                            if (movimentacao["emitir_nota_fiscal"]) {
                                                return response.json().then(data => {
                                                    let comprovante_id = data.comprovante;
                                                    fetch(`/api/vendas/${venda_id}/nota_fiscal_da_venda/`, {
                                                        headers: {
                                                            "X-CSRFToken": csrf_token,
                                                        },
                                                        method: "POST"
                                                    })
                                                    .then(response => {
                                                        if (response.ok) {
                                                            return response.json().then(data => {
                                                                swal.fire({
                                                                    title: "Comprovante e nota fiscal emitidos com sucesso!",
                                                                    text: "Deseja imprimir o comprovante?",
                                                                    icon: "success",
                                                                    showCancelButton: true,
                                                                    confirmButtonText: "Imprimir",
                                                                    cancelButtonText: "Fechar"
                                                                })
                                                                .then(res => {
                                                                    if (res.isConfirmed) {
                                                                        window.open("/financeiro/comprovantes/"+comprovante_id, "_blank");
                                                                    }
                                                                    swal.fire({
                                                                        title: "Comprovante impresso!",
                                                                        text: "Deseja imprimir a nota fiscal?",
                                                                        icon: "success",
                                                                        showCancelButton: true,
                                                                        confirmButtonText: "Imprimir",
                                                                        cancelButtonText: "Fechar"
                                                                    })
                                                                    .then(res => {
                                                                        if (res.isConfirmed) {
                                                                            window.open("/financeiro/notas_fiscais/"+data.nota_fiscal, "_blank");
                                                                        }
                                                                        window.location.reload();
                                                                    })
                                                                })
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
                                                    });
                                                });
                                            }
                                            else {
                                                swal.fire({
                                                    title: "Comprovante emitido com sucesso!",
                                                    text: "Deseja imprimir o comprovante?",
                                                    icon: "success",
                                                    showCancelButton: true,
                                                    confirmButtonText: "Imprimir",
                                                    cancelButtonText: "Fechar"
                                                })
                                                .then(res => {
                                                    if (res.isConfirmed) {
                                                        return response.json().then(data => {
                                                            window.open("/financeiro/comprovantes/"+data.comprovante, "_blank");
                                                            window.location.reload();
                                                        })
                                                    }
                                                    window.location.reload();
                                                })
                                            }
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
                            }
                            else {
                                if (movimentacao["emitir_nota_fiscal"]) {
                                    return response.json().then(data => {
                                        swal.fire({
                                            title: "Venda salva com sucesso!",
                                            text: "Emitindo comprovante...",
                                            icon: "info",
                                            showConfirmButton: false,
                                            allowOutsideClick: false
                                        })
    
                                        fetch(`/api/vendas/${data.venda_id}/nota_fiscal_da_venda/`, {
                                            headers: {
                                                "X-CSRFToken": csrf_token,
                                            },
                                            method: "POST"
                                        })
                                        .then(response => {
                                            if (response.ok) {
                                                return response.json().then(data => {
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
                                                            window.open("/financeiro/notas_fiscais/"+data.nota_fiscal, "_blank");
                                                            window.location.reload();
                                                        }
                                                        window.location.reload();
                                                    })
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
                                        });
                                    });
                                }
                                else {
                                    swal.fire({
                                        title: "Venda salva com sucesso!",
                                        icon: "success"
                                    }).then(() => {
                                        window.location.reload();
                                    });
                                }
                            }
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

    editar_venda_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let movimentacao_id = button.getAttribute('data-id');
            fetch(`/api/vendas/${movimentacao_id}/`, {
                method: "GET"
            })
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        modal_editar_venda.querySelector("#cliente").value = data.cliente;
                        modal_editar_venda.querySelector("#cliente_endereco").value = data.cliente_endereco;
                        modal_editar_venda.querySelector("#vendedor").value = data.vendedor;
                        modal_editar_venda.querySelector("#metodo_pagamento").value = data.metodo_pagamento;
                        modal_editar_venda.querySelector("#subtotal").value = (data.valor_de_venda_dos_produtos).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        modal_editar_venda.querySelector("#valor_de_custo_dos_produtos").value = (data.valor_de_custo_dos_produtos).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        modal_editar_venda.querySelector("#taxas").value = (data.taxas).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        modal_editar_venda.querySelector("#desconto").value = (data.desconto).toLocaleString('pt-BR', {minimumFractionDigits: 2});

                        for (let produto_transacao of data.produtos_transacao) {
                            let linha_produto = document.querySelector(`.produto_editar [data-id="${produto_transacao.produto}"]`).closest('tr');
                            linha_produto.querySelector('#checkbox_produto').checked = true;
                            linha_produto.querySelector('#quantidade').value = produto_transacao.quantidade;
                            linha_produto.querySelector('#valor_custo').value = (produto_transacao.valor_custo).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                            linha_produto.querySelector('#valor_venda').value = (produto_transacao.valor_venda).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                            linha_produto.querySelector('#valor_total_custo').value = ((produto_transacao.valor_custo * produto_transacao.quantidade)).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                            linha_produto.querySelector('#valor_total_venda').value = ((produto_transacao.valor_venda * produto_transacao.quantidade)).toLocaleString('pt-BR', {minimumFractionDigits: 2});
                        }

                        salvar_editar_venda.dataset.id = movimentacao_id;
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

    salvar_editar_venda.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_editar_venda.checkValidity()) {
            swal.fire({
                title: "Venda validada com sucesso!",
                text: "Clique em 'Confirmar' para salvar a venda.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let cliente = modal_editar_venda.querySelector("#cliente").value;
                let cliente_endereco = modal_editar_venda.querySelector("#cliente_endereco").value;
                let vendedor = modal_editar_venda.querySelector("#vendedor").value;
                let metodo_pagamento = modal_editar_venda.querySelector("#metodo_pagamento").value;
                let valor_de_venda_dos_produtos = modal_editar_venda.querySelector("#subtotal").value.replace(/\D/g, '')/100;
                let valor_de_custo_dos_produtos = modal_editar_venda.querySelector("#valor_de_custo_dos_produtos").value.replace(/\D/g, '')/100;
                let taxas = modal_editar_venda.querySelector("#taxas").value.replace(/\D/g, '')/100;
                let desconto = modal_editar_venda.querySelector("#desconto").value.replace(/\D/g, '')/100;
                let valor_total_pago = valor_de_custo_dos_produtos;
                let valor_total_recebido = (valor_de_venda_dos_produtos + taxas - desconto).toFixed(2);

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
                            'tipo': 's'
                        })
                    }
                }

                tipo = produtos_transacao.length ? 'v' : 'p';

                let movimentacao = {
                    cliente,
                    cliente_endereco,
                    vendedor,
                    valor_total_recebido,
                    valor_total_pago,
                    valor_de_venda_dos_produtos,
                    valor_de_custo_dos_produtos,
                    tipo,
                    taxas,
                    desconto,
                    metodo_pagamento
                };

                let movimentacao_id = salvar_editar_venda.dataset.id;
                let formData = new FormData(form_editar_venda);
                formData.append("transacao", JSON.stringify(movimentacao));
                formData.append("produtos_transacao", JSON.stringify(produtos_transacao));

                if (result.isConfirmed) {
                    fetch(`/api/vendas/${movimentacao_id}/`, {
                        method: "PUT",
                        headers: {
                            "X-CSRFToken": csrf_token,
                        },
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Venda salva com sucesso!",
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
                    });
                }
            });
        } else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error",
            })
        }
    });

    excluir_venda_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let movimentacao_id = button.getAttribute('data-id');
            swal.fire({
                title: "Tem certeza que deseja excluir a venda?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/api/movimentacoes/${movimentacao_id}/`, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf_token,
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Venda excluída com sucesso!",
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
        let linhas_produto = document.querySelectorAll('.produto_cadastro, .produto_estoque_cadastro');
        let valor_de_custo_dos_produtos = 0;
        let subtotal = 0;

        for (let linha_produto of linhas_produto) {
            if (linha_produto.querySelector('input[type=checkbox]').checked) {
                let valor_custo_total = linha_produto.querySelector('#valor_total_custo');
                let valor_venda_total = linha_produto.querySelector('#valor_total_venda');
                valor_de_custo_dos_produtos += parseFloat(valor_custo_total.value.replace(/\D/g, '')/100);
                subtotal += parseFloat(valor_venda_total.value.replace(/\D/g, '')/100);
            }
        }

        modal_cadastro_venda.querySelector('#subtotal').value = subtotal.toLocaleString('pt-BR', {minimumFractionDigits: 2});
        modal_cadastro_venda.querySelector('#valor_de_custo_dos_produtos').value = valor_de_custo_dos_produtos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
    else {
        let linhas_produto = document.querySelectorAll('.produto_editar');
        let valor_de_custo_dos_produtos = 0;
        let subtotal = 0;

        for (let linha_produto of linhas_produto) {
            let valor_custo_total = linha_produto.querySelector('#valor_total_custo');
            let valor_venda_total = linha_produto.querySelector('#valor_total_venda');
            valor_de_custo_dos_produtos += parseFloat(valor_custo_total.value.replace(/\D/g, '')/100);
            subtotal += parseFloat(valor_venda_total.value.replace(/\D/g, '')/100);
        }

        modal_editar_venda.querySelector('#subtotal').value = subtotal.toLocaleString('pt-BR', {minimumFractionDigits: 2});
        modal_editar_venda.querySelector('#valor_de_custo_dos_produtos').value = valor_de_custo_dos_produtos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
}
