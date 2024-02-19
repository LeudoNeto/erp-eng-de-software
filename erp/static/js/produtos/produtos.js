document.addEventListener("DOMContentLoaded", function() {
    var salvar_produto = document.querySelector('#salvar_produto');
    var form_produto = document.querySelector('#form_criar_produto');
    var editar_produto_buttons = document.querySelectorAll('#editar_produto');
    var form_editar_produto = document.querySelector('#form_editar_produto');
    var salvar_editar_produto = document.querySelector('#salvar_editar_produto');
    var excluir_produto_buttons = document.querySelectorAll('#excluir_produto');

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
                        swal.close();
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

            fetch(`/api/produtos/${produto_id}/get_produto_foto`)
            .then(response => {
                if (response.ok) {
                    return response.blob().then(blob => {
                        let frame = form_editar_produto.querySelector('#frame_editar');
                        frame.src = URL.createObjectURL(blob);
                        frame.hidden=false;
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

                if (result.isConfirmed) {
                    fetch(`/api/produtos/${produto_id}/`, {
                        method: "PUT",
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
                        method: "DELETE"
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

function preview(editar=false) {
    if (editar) {
        let frame_editar = document.getElementById('frame_editar');
        frame_editar.src = URL.createObjectURL(event.target.files[0]);
        frame_editar.hidden=false;
    }
    else {
        let frame = document.getElementById('frame');
        frame.src = URL.createObjectURL(event.target.files[0]);
        frame.hidden=false;
    }
}
function clearImage(editar=false) {
    if (editar) {
        document.getElementById('formFile_editar').value = null;
        let frame_editar = document.getElementById('frame_editar');
        frame_editar.src = "";
        frame_editar.hidden=true;
    }
    else {
        document.getElementById('formFile').value = null;
        let frame = document.getElementById('frame');
        frame.src = "";
        frame.hidden=true;
    }
}