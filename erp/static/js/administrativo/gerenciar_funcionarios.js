document.addEventListener("DOMContentLoaded", function() {
    var salvar_usuario = document.querySelector('#salvar_usuario');
    var form_criar_usuario = document.querySelector('#form_criar_usuario');
    var excluir_usuario_buttons = document.querySelectorAll('#excluir_usuario');
    var telefone_input = document.querySelector('#telefone');
    $(telefone_input).inputmask({mask: '(99) 99999-9999'});

    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    salvar_usuario.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_criar_usuario.querySelector('#password').value != form_criar_usuario.querySelector('#confirmar_senha').value) {
            swal.fire({
                title: "Senhas não conferem",
                text: "As senhas digitadas não conferem.",
                icon: "error"
            });
            return;
        }

        if (form_criar_usuario.checkValidity() && telefone_input.inputmask.isComplete()) {
            swal.fire({
                title: "Dados validados com sucesso!",
                text: "Clique em 'Confirmar' para salvar o funcionário.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_criar_usuario);

                if (result.isConfirmed) {
                    fetch("/api/usuarios/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Funcionário cadastrado com sucesso!",
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
                            title: "Erro ao salvar o funcionário",
                            text: error,
                            icon: "error"
                        });
                    });
                }
            });
        }
        else {
            swal.fire({
                title: "Campos obrigatórios não preenchidos",
                text: "Preencha todos os campos obrigatórios para salvar o funcionário.",
                icon: "error"
            });
        }
    });

    excluir_usuario_buttons.forEach(button => {
        button.addEventListener('click', function() {
            swal.fire({
                title: "Tem certeza que deseja excluir o funcionário?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/api/usuarios/${button.dataset.id}/`, {
                        headers: {
                            'X-CSRFToken': csrf_token
                        },
                        method: "DELETE"
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Funcionário excluído com sucesso!",
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
                    })
                    .catch(error => {
                        swal.fire({
                            title: "Erro ao excluir o funcionário",
                            text: error,
                            icon: "error"
                        });
                    });
                }
            });
        });
    });

});
