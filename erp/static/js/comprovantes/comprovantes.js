document.addEventListener("DOMContentLoaded", function() {
    var modal_emitir_comprovante = document.querySelector("#modal_emitir_comprovante");
    var form_emitir_comprovante = document.querySelector("#form_emitir_comprovante");
    var botao_emitir_comprovante = modal_emitir_comprovante.querySelector("#botao_emitir_comprovante");

    var excluir_comprovante_buttons = document.querySelectorAll("#excluir_comprovante")

    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    botao_emitir_comprovante.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_emitir_comprovante.checkValidity()) {
            swal.fire({
                title: "Comprovante validado com sucesso!",
                text: "Clique em 'Confirmar' para emitir o comprovante.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let produtos_comprovante = [];
                let linhas_produtos_produtos_comprovante = document.querySelectorAll('.produto_vendido_emitir');
                for (let linha_produto of linhas_produtos_produtos_comprovante) {
                    if (linha_produto.querySelector('input[type=checkbox]').checked) {
                        produtos_comprovante.push({
                            'produto': linha_produto.querySelector('input[type=checkbox]').dataset.id,
                            'valor_unitario': linha_produto.querySelector('#valor_unitario').value.replace(/\D/g, '')/100,
                            'valor_total': linha_produto.querySelector('#valor_total').value.replace(/\D/g, '')/100,
                            'quantidade': linha_produto.querySelector('#quantidade').value,
                        })
                    }
                }

                let formData = new FormData(form_emitir_comprovante);

                let subtotal = form_emitir_comprovante.querySelector('#subtotal').value.replace(/\D/g, '')/100
                let taxas = form_emitir_comprovante.querySelector('#taxas').value.replace(/\D/g, '')/100
                let desconto = form_emitir_comprovante.querySelector('#desconto').value.replace(/\D/g, '')/100


                formData.append("subtotal", subtotal);
                formData.append("taxas", taxas);
                formData.append("desconto", desconto);
                formData.append("total", subtotal+taxas-desconto);

                formData.append("produtos_comprovante", JSON.stringify(produtos_comprovante));

                if (result.isConfirmed) {
                    fetch("/api/comprovantes/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
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

    excluir_comprovante_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let comprovante_id = button.getAttribute('data-id');
            swal.fire({
                title: "Tem certeza que deseja excluir o comprovante?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch("/api/comprovantes/" + comprovante_id, {
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrf_token
                        },
                        method: "DELETE"
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Comprovante excluído com sucesso!",
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

        modal_emitir_comprovante.querySelector('#subtotal').value = valor_produtos_vendidos.toLocaleString('pt-BR', {minimumFractionDigits: 2});
    }
}
