document.addEventListener("DOMContentLoaded", function() {
    var salvar_cargo = document.querySelector('#salvar_cargo');
    var form_criar_cargo = document.querySelector('#form_criar_cargo');

    var editar_cargo_buttons = document.querySelectorAll('#editar_cargo');
    var form_editar_cargo = document.querySelector('#form_editar_cargo');
    var salvar_editar_cargo = document.querySelector('#salvar_editar_cargo');

    var excluir_cargo_buttons = document.querySelectorAll('#excluir_cargo');

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_cargo.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

        if (form_criar_cargo.checkValidity()){
            swal.fire({
                title: "Dados validados com sucesso!",
                text: "Clique em 'Confirmar' para salvar o cargo.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_criar_cargo);

                if (result.isConfirmed) {
                    fetch("/api/cargos/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Cargo criado com sucesso!",
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
                    .catch(error => {
                        swal.fire({
                            title: "Erro ao salvar o cargo",
                            text: error,
                            icon: "error"
                        });
                    });
                }
            });
        }
        else {
            swal.fire({
                title: "Erro ao validar campos",
                text: "Verifique se todos os campos obrigatórios foram preenchidos.",
                icon: "error"
            });
        }
    });

    editar_cargo_buttons.forEach(button => {
        button.addEventListener('click', function() {
            salvar_editar_cargo.dataset.id = button.dataset.id;
            swal.fire({
                title: "Carregando dados do cargo",
                icon: "info"
            });
            fetch(`/api/cargos/${button.dataset.id}/`)
            .then(response => {
                if (response.ok) {
                    return response.json().then(data => {
                        form_editar_cargo.querySelector('#nome').value = data.nome;
                        form_editar_cargo.querySelector('#descricao').value = data.descricao;
                        form_editar_cargo.querySelector('#nivel_acesso').value = data.nivel_acesso;
                        swal.close();
                    })
                    .catch(error => {
                        swal.fire({
                            title: "Erro ao carregar dados do cargo",
                            text: error,
                            icon: "error"
                        });
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

    salvar_editar_cargo.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        });

        if (form_editar_cargo.checkValidity()) {
            swal.fire({
                title: "Dados validados com sucesso!",
                text: "Clique em 'Confirmar' para salvar as alterações.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_editar_cargo);

                if (result.isConfirmed) {
                    fetch(`/api/cargos/${salvar_editar_cargo.dataset.id}/`, {
                        method: "PUT",
                        headers: {
                            'X-CSRFToken': csrf_token
                        },
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Cargo atualizado com sucesso!",
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
                    .catch(error => {
                        swal.fire({
                            title: "Erro ao salvar as alterações",
                            text: error,
                            icon: "error"
                        });
                    });
                }
            });
        }
        else {
            swal.fire({
                title: "Erro ao validar campos",
                text: "Verifique se todos os campos obrigatórios foram preenchidos.",
                icon: "error"
            });
        }
    });

    excluir_cargo_buttons.forEach(button => {
        button.addEventListener('click', function() {
            swal.fire({
                title: "Tem certeza que deseja excluir o cargo?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/api/cargos/${button.dataset.id}/`, {
                        headers: {
                            'X-CSRFToken': csrf_token
                        },
                        method: "DELETE"
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Cargo excluído com sucesso!",
                                icon: "success"
                            }).then(() => {
                                button.closest('.cargo').remove();
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
                    .catch(error => {
                        swal.fire({
                            title: "Erro ao excluir o cargo",
                            text: error,
                            icon: "error"
                        });
                    });
                }
            });
        });
    });

});
