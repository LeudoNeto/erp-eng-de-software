document.addEventListener("DOMContentLoaded", function() {
    var modal_criar_usuario = document.querySelector('#modal_criar_usuario');
    var salvar_usuario = modal_criar_usuario.querySelector('#salvar_usuario');
    var form_criar_usuario = modal_criar_usuario.querySelector('#form_criar_usuario');
    var telefone_input = modal_criar_usuario.querySelector('#telefone');
    $(telefone_input).inputmask({mask: '(99) 99999-9999'});

    var editar_usuario_buttons = document.querySelectorAll('#editar_usuario');
    var modal_editar_usuario = document.querySelector('#modal_editar_usuario');
    var salvar_editar_usuario = modal_editar_usuario.querySelector('#salvar_usuario');
    var form_editar_usuario = modal_editar_usuario.querySelector('#form_editar_usuario');
    var telefone_editar_input = modal_editar_usuario.querySelector('#telefone');
    $(telefone_editar_input).inputmask({mask: '(99) 99999-9999'});

    var excluir_usuario_buttons = document.querySelectorAll('#excluir_usuario');
    
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

    editar_usuario_buttons.forEach(button => {
        button.addEventListener('click', function() {
            salvar_editar_usuario.dataset.id = button.dataset.id;
            fetch(`/api/usuarios/${button.dataset.id}/`)
            .then(response => {
                if (response.ok) {
                    return response.json();
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
            .then(data => {
                modal_editar_usuario.querySelector('#nome').value = data.nome;
                modal_editar_usuario.querySelector('#email').value = data.email;
                modal_editar_usuario.querySelector('#telefone').value = data.telefone;
                modal_editar_usuario.querySelector('#cargo').value = data.cargo;
                modal_editar_usuario.querySelector('#foto').value = null;
                if (data.foto) {
                    let preview_imagem = modal_editar_usuario.querySelector('#preview_imagem');
                    preview_imagem.src = data.foto;
                    preview_imagem.hidden=false;
                }
                else {
                    let preview_imagem = modal_editar_usuario.querySelector('#preview_imagem');
                    preview_imagem.src = "";
                    preview_imagem.hidden=true;
                }
            })
            .catch(error => {
                swal.fire({
                    title: "Erro ao buscar o funcionário",
                    text: error,
                    icon: "error"
                });
            });
        });
    });

    salvar_editar_usuario.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"
        })

        if (form_editar_usuario.querySelector('#password').value != form_editar_usuario.querySelector('#confirmar_senha').value) {
            swal.fire({
                title: "Senhas não conferem",
                text: "As senhas digitadas não conferem. Se você não deseja alterar a senha do usuário, apenas apague os campos de senha e confirmação.",
                icon: "error"
            });

            return;
        }

        if (form_editar_usuario.checkValidity() && telefone_editar_input.inputmask.isComplete()) {
            swal.fire({
                title: "Dados validados com sucesso!",
                text: "Clique em 'Confirmar' para salvar as alterações do funcionário.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_editar_usuario);

                if (result.isConfirmed) {
                    fetch(`/api/usuarios/${salvar_editar_usuario.dataset.id}/`, {
                        method: "PUT",
                        headers: {
                            'X-CSRFToken': csrf_token
                        },
                        body: formData
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Funcionário atualizado com sucesso!",
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
                            title: "Erro ao salvar as alterações do funcionário",
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
                text: "Preencha todos os campos obrigatórios para salvar as alterações do funcionário.",
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