document.addEventListener("DOMContentLoaded", function() {
    var salvar_produto = document.querySelector('#salvar_produto');
    var form_adicionar_produto = document.querySelector('#form_adicionar_produto');

    var editar_produto_buttons = document.querySelectorAll('#editar_produto');
    var form_editar_produto = document.querySelector('#form_editar_produto');
    var salvar_editar_produto = document.querySelector('#salvar_editar_produto');

    var remover_produto_buttons = document.querySelectorAll('#remover_produto');

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_produto.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

        if (form_adicionar_produto.checkValidity()) {
            swal.fire({
                title: "Produto validado com sucesso!",
                text: "Clique em 'Confirmar' para salvar o produto.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_adicionar_produto);

                if (result.isConfirmed) {
                    fetch("/api/produtos_estoque/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produto adicionado com sucesso!",
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

    editar_produto_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let produto_id = button.getAttribute('data-id');
            salvar_editar_produto.dataset.id = produto_id;

            swal.fire({
                title: "Carregando dados do produto",
                icon: "info"
            });
            fetch(`/api/produtos_estoque/${produto_id}/`)
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        form_editar_produto.querySelector('#produto').value = data.produto;
                        form_editar_produto.querySelector('#descricao').value = data.descricao;
                        form_editar_produto.querySelector('#quantidade').value = data.quantidade;
                        form_editar_produto.querySelector('#valor_custo').value = data.valor_custo;
                        form_editar_produto.querySelector('#valor_venda').value = data.valor_venda;
                        form_editar_produto.querySelector('#localizacao').value = data.localizacao;
                        swal.close();
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
        });
    });

    salvar_editar_produto.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        });

        if (form_editar_produto.checkValidity()) {
            swal.fire({
                title: "Produto validado com sucesso!",
                text: "Clique em 'Confirmar' para salvar o produto.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let produto_id = salvar_editar_produto.dataset.id;
                let formData = new FormData(form_editar_produto);

                if (result.isConfirmed) {
                    fetch(`/api/produtos_estoque/${produto_id}/`, {
                        method: "PUT",
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produto editado com sucesso!",
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
        }
        else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error"
            });
        }
    });

    remover_produto_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let produto_id = button.getAttribute('data-id');

            swal.fire({
                title: "Remover produto",
                text: `Tem certeza que deseja remover o produto do estoque?`,
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Sim",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/api/produtos_estoque/${produto_id}/`, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf_token
                        }

                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produto removido com sucesso!",
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
