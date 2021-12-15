var camposValidosEmbalagem = false;
var listaEmbalagens = [];
var listaEmbs = [];
var listaExistentes = [];
var check = 0;
var mensagens = [];

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposEmbalagem();
    if (camposValidosEmbalagem) {
        $(".loader").toggle();
        $("#form_embalagem").submit();
    }
});

$("#add_embalagem").click(function(event) {
    event.preventDefault();
    var pesoCorte = $("#peso_corte").val();
    var tipoCorte = $("input[name=tipo_corte]:checked").val();
    var flag = false;
    if (pesoCorte != "" && tipoCorte != "") {
        for (let i = 0; i < listaEmbalagens.length; i++) {
            if (pesoCorte == listaEmbalagens[i].peso_corte && tipoCorte == listaEmbalagens[i].tipo_corte) {
                flag = true;
                break
            }
        }
        if (flag) {
            alert("Embalagem já inserida para cadastro!");
        } else {
            if (listaEmbalagens.length == 0) {
                $("#tabela_embalagens tbody").html("");
            }
            var embalagem = {
                "peso_corte": pesoCorte,
                "tipo_corte": tipoCorte
            };
            var tipoCorteExibido = "";
            switch (tipoCorte) {
                case "CF":
                    tipoCorteExibido = "Contrafilé";
                    break;
                case "FR":
                    tipoCorteExibido = "Fraldinha";
                    break;
                case "FM":
                    tipoCorteExibido = "Filé-mignon";
                    break;
                case "PC":
                    tipoCorteExibido = "Picanha";
                default:
                    break;
            }
            $("#tabela_embalagens tbody").append(`
                <tr>
                    <td scope="col">${embalagem.peso_corte}</td>
                    <td scope="col">${tipoCorteExibido}</td>
                    <td scope="col"><button class="btn btn-danger" style="border-radius: 2rem;" onclick="removeLinhaTabEmbalagem(this)"><i class="fa fa-times-circle"></i></button>
                </tr>
            `);
            listaEmbalagens.push(embalagem);
            $("#modal-embalagem").modal('hide');
            $("#peso_corte").val("");
            $("#tipo_corte").val("");
        }
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
});

function validaCamposEmbalagem() {
    var idAnimal = $("#animal").val();
    var dataEmbalagem = $("#data_embalagem").val();
    if (idAnimal != "" && dataEmbalagem != "" && listaEmbalagens.length > 0) {
        $("#lista_embalagens").val(JSON.stringify(listaEmbalagens));
        camposValidosEmbalagem = true;

    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

function removeLinhaTabEmbalagem(obj) {
    var embalagemRemovida = [];
    $(obj).parent().parent().children().each(function() {
        embalagemRemovida.push($(this).text());
    });
    var tipoCorte = "";
    switch (embalagemRemovida[1]) {
        case "Contrafilé":
            tipoCorte = "CF";
            break;
        case "Fraldinha":
            tipoCorte = "FR";
            break;
        case "Filé-mignon":
            tipoCorte = "FM";
            break;
        case "Picanha":
            tipoCorte = "PC";
        default:
            break;
    }

    function encontraEmbalagem(elemento) {
        if (elemento.peso_corte == embalagemRemovida[0] && elemento.tipo_corte == tipoCorte) {
            return true;
        }
        return false;
    }
    var i = listaEmbalagens.findIndex(encontraEmbalagem);
    if (i != -1) {
        $(obj).parent().parent().remove();
        listaEmbalagens.splice(i, 1);
        if (listaEmbalagens.length == 0) {
            $("#tabela_embalagens tbody").html(`
                <tr>
                    <td colspan="3">Não há embalagens inseridas.</td>
                </tr>
            `);
        }
    } else {
        alert("Erro ao remover a embalagem!");
    }
    console.log(listaEmbalagens);
}

$(document).ready(function() {
    $('#form_embalagem').submit(function(event) {
        var formData = new FormData($(this)[0]);
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: formData,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            async: true,

            success: function(result) {
                result = JSON.parse(result);
                if (result.resposta == 'OK') {
                    verificaStatusTasks(result.tasks_ids);
                } else {
                    $(".loader").toggle();
                    alert("Erro interno! Tente novamente mais tarde.");
                }
            },
            fail: function(msg) {
                $(".loader").toggle();
                alert("Erro ao salvar!");
            },
            beforeSend: function() {},
            complete: function(msg) {},
            error: function(msg) {
                $(".loader").toggle();
                alert("Erro interno!");
            }
        });
        event.preventDefault();
    });
});

function verificaStatusTasks(listaTasks) {
    listaEmbs = listaTasks;

    for (let i = 0; i < listaTasks.length; i++) {
        if (listaTasks[i].task_id != -1) {
            getStatus(listaTasks[i].task_id);
        } else {
            listaExistentes.push(listaTasks[i]);
        }
    }
}

function getStatus(taskID) {
    $.ajax({
            url: `/tasks/${taskID}/`,
            method: 'GET'
        })
        .done((res) => {
            const taskStatus = res.task_status;

            if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') {
                var mensagem = "";
                const taskResult = res.task_result;
                console.log(taskResult);
                if (taskResult == "OK") {
                    mensagem = "Embalagem cadastrada com sucesso!";
                } else if (taskResult == "ERRO_DADOS") {
                    mensagem = "Erro no salvamento dos dados!";
                } else if (taskResult == "ERRO_BLOCKCHAIN") {
                    mensagem = "Erro ao salvar o dado na blockchain!";
                } else {
                    mensagem = "Erro interno durante a tarefa assíncrona!";
                }
                check += 1;
                for (let i = 0; i < listaEmbs.length; i++) {
                    if (res.task_id == listaEmbs[i].task_id) {
                        mensagens.push({
                            "id_embalagem": listaEmbs[i].id_embalagem,
                            "mensagem": mensagem
                        })
                    }
                }
                if (check == listaEmbs.length - listaExistentes.length) {
                    $(".loader").toggle();
                    const quebraLinha = "\r\n";
                    var msg = "";
                    for (let i = 0; i < mensagens.length; i++) {
                        msg += `Embalagem ${mensagens[i].id_embalagem+1}: ${mensagens[i].mensagem}`;
                        msg += quebraLinha;
                    }
                    for (let i = 0; i < listaExistentes.length; i++) {
                        msg += `Embalagem ${listaExistentes[i].id_embalagem+1}: Embalagem já cadastrada`;
                        msg += quebraLinha;
                    }
                    alert(msg);
                    location.href = "/";
                }
            } else {
                setTimeout(function() {
                    getStatus(res.task_id);
                }, 1000);
            }
        })
        .fail((err) => {
            $(".loader").toggle();
            console.log(err);
            alert("Erro interno!");
        });
}