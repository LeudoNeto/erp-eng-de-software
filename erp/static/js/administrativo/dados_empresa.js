document.addEventListener("DOMContentLoaded", function() {
    var botao_salvar = document.querySelector('#botao_salvar');
    var form_dados_empresa = document.querySelector('#form_dados_empresa');
    var empresa_id = document.querySelector('#empresa_id').value;
    var cnpj_input = document.querySelector('#cnpj');
    var telefone_input = document.querySelector('#telefone');
    var telefone_whatsapp_input = document.querySelector('#telefone_whatsapp');
    $(cnpj_input).inputmask({mask: '99.999.999/9999-99'});
    $(telefone_input).inputmask({mask: '(99) 99999-9999'});
    $(telefone_whatsapp_input).inputmask({mask: '(99) 99999-9999'});

    botao_salvar.addEventListener('click', function() {
        swal.fire({
            title: "Verificando campos obrigatórios",
            icon: "info"    
        })

        if (form_dados_empresa.checkValidity()
            && cnpj_input.inputmask.isComplete()
            && telefone_input.inputmask.isComplete()
            && (!telefone_whatsapp_input.value || telefone_whatsapp_input.inputmask.isComplete())
        ){
            swal.fire({
                title: "Dados validados com sucesso!",
                text: "Clique em 'Confirmar' para salvar os dados.",
                icon: "success",
                confirmButtonText: "Confirmar",
                showCancelButton: true,
                cancelButtonText: "Cancelar"
            }).then((result) => {
                let formData = new FormData(form_dados_empresa);
                let jsonForm = {};

                formData.forEach((value, key) => {
                    jsonForm[key] = value;
                });

                if (result.isConfirmed) {
                    fetch(`/api/empresas/${empresa_id}/`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": jsonForm.csrfmiddlewaretoken
                        },
                        body: JSON.stringify(jsonForm)
                
                    })
                    .then(response => {
                        if (response.ok) {
                            swal.fire({
                                title: "Dados salvos com sucesso!",
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
                icon: "error",
            })
        }

    });

});
