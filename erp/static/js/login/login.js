document.addEventListener("DOMContentLoaded", function() {
    var botao_login = document.querySelector('#botao_login');
    var form_login = document.querySelector('#form_login');

    botao_login.addEventListener('click', function() {

        if (email.value == '' || senha.value == '') {
            swal.fire({
                title: "Preencha os campos obrigatórios",
                icon: "error"
            });
        } else {
            let formData = new FormData(form_login);

            fetch("/api/login/", {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    swal.fire({
                        title: "Login efetuado com sucesso!",
                        icon: "success"
                    });
                    window.location.href = "/";
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
    

});
