document.addEventListener("DOMContentLoaded", function() {
    var salvar_produto = document.querySelector('#salvar_produto');
    var form_produto = document.querySelector('#form_criar_produto');

    var editar_produto_buttons = document.querySelectorAll('#editar_produto');
    var form_editar_produto = document.querySelector('#form_editar_produto');
    var salvar_editar_produto = document.querySelector('#salvar_editar_produto');

    var excluir_produto_buttons = document.querySelectorAll('#excluir_produto');

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_produto.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

        if (form_produto.checkValidity()) {
            swal.fire({
                title: "Produto validado com sucesso!",
                text: "Clique em 'Confirmar' para salvar o produto.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_produto);
                formData.append('valor_custo_padrao', formData.get('valor_custo_padrao').replace(/\D/g, '')/100);
                formData.append('valor_venda_padrao', formData.get('valor_venda_padrao').replace(/\D/g, '')/100);
                formData.append('aliquota_icms', formData.get('aliquota_icms').replace(/\D/g, '')/10);

                if (result.isConfirmed) {
                    fetch("/api/produtos/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produto salvo com sucesso!",
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

    // preencher formulário de edição com dados do produto
    editar_produto_buttons.forEach(button => {
        button.addEventListener('click', function() {

            swal.fire({
                title: "Carregando dados do produto",
                icon: "info"
            });

            let produto_id = button.getAttribute('data-id');
            fetch(`/api/produtos/${produto_id}/`)
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        form_editar_produto.querySelector('#nome').value = data.nome;
                        form_editar_produto.querySelector('#descricao').value = data.descricao;
                        form_editar_produto.querySelector('#codigo_referencia').value = data.codigo_referencia;
                        form_editar_produto.querySelector('#valor_custo_padrao').value = data.valor_custo_padrao;
                        form_editar_produto.querySelector('#valor_venda_padrao').value = data.valor_venda_padrao;
                        form_editar_produto.querySelector('#aliquota_icms').value = data.aliquota_icms;
                        swal.close();
                        if (data.foto) {
                            let preview_imagem = form_editar_produto.querySelector('#preview_imagem');
                            preview_imagem.src = data.foto;
                            preview_imagem.hidden=false;
                        }
                        else {
                            let preview_imagem = form_editar_produto.querySelector('#preview_imagem');
                            preview_imagem.src = "";
                            preview_imagem.hidden=true;
                        }
                        salvar_editar_produto.dataset.id = produto_id;
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

    salvar_editar_produto.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

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
                formData.append('valor_custo_padrao', formData.get('valor_custo_padrao').replace(/\D/g, '')/100);
                formData.append('valor_venda_padrao', formData.get('valor_venda_padrao').replace(/\D/g, '')/100);
                formData.append('aliquota_icms', formData.get('aliquota_icms').replace(/\D/g, '')/10);

                if (result.isConfirmed) {
                    fetch(`/api/produtos/${produto_id}/`, {
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
        } else {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error",
            })
        }

    });


    excluir_produto_buttons.forEach(button => {
        button.addEventListener('click', function() {
            let produto_id = button.getAttribute('data-id');
            swal.fire({
                title: "Tem certeza que deseja excluir o produto?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch("/api/produtos/" + produto_id, {
                        method: "DELETE",
                        headers: {
                            "X-CSRFToken": csrf_token
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Produto excluído com sucesso!",
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

function formatarICMS(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, '');
    valor = (valor / 10).toLocaleString('pt-BR', {minimumFractionDigits: 1});
    input.value = valor;
}

function preview(botao) {
    let modal = botao.closest('.modal');
    let preview_imagem = modal.querySelector('#preview_imagem');
    preview_imagem.src = URL.createObjectURL(botao.files[0]);
    preview_imagem.hidden=false;
}
function clearImage(botao) {
    let modal = botao.closest('.modal');
    modal.querySelector('#foto').value = null;
    let preview_imagem = modal.querySelector('#preview_imagem');
    preview_imagem.src = "";
    preview_imagem.hidden=true;
}