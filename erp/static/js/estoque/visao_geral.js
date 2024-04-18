document.addEventListener("DOMContentLoaded", function() {
    var salvar_produto = document.querySelector('#salvar_produto');
    var form_adicionar_produto = document.querySelector('#form_adicionar_produto');

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


});

function formatarMoeda(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, '');
    valor = (valor / 100).toLocaleString('pt-BR', {minimumFractionDigits: 2});
    input.value = valor;
}
