var camposValidosVacina = false;
var listaVacinas = [];
var listaVacs = [];
var listaExistentes = [];
var check = 0;
var mensagens = [];

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposVacina();
    if (camposValidosVacina) {
        $(".loader").toggle();
        $("#form_vacina").submit();
    }
});

$("#add_vacina").click(function(event) {
    event.preventDefault();
    var especificidade = $("#especificidade").val();
    var lote = $("#lote").val();
    var dose = $("#dose").val();
    var dataAplicacao = $("#data_aplicacao").val();
    var flag = false;
    if (especificidade != "" && lote != "" && dose != "" && dataAplicacao != "") {
        for (let i = 0; i < listaVacinas.length; i++) {
            if (especificidade == listaVacinas[i].especificidade && lote == listaVacinas[i].lote && dose == listaVacinas[i].dose && dataAplicacao == listaVacinas[i].data_aplicacao) {
                flag = true;
                break
            }
        }
        if (flag) {
            alert("Vacina já inserida para cadastro!");
        } else {
            if (listaVacinas.length == 0) {
                $("#tabela_vacinas tbody").html("");
            }
            var vacina = {
                "especificidade": especificidade,
                "lote": lote,
                "dose": dose,
                "data_aplicacao": dataAplicacao
            };
            var dataTemp = vacina.data_aplicacao.split("-");
            $("#tabela_vacinas tbody").append(`
                <tr>
                    <td scope="col">${vacina.especificidade}</td>
                    <td scope="col">${vacina.lote}</td>
                    <td scope="col">${vacina.dose}</td>
                    <td scope="col">${dataTemp[2]+"/"+dataTemp[1]+"/"+dataTemp[0]}</td>
                    <td scope="col"><button class="btn btn-danger" style="border-radius: 2rem;" onclick="removeLinha(this)"><i class="fa fa-times-circle"></i></button>
                </tr>
            `);
            listaVacinas.push(vacina);
            $("#modal-vacina").modal('hide');
            $("#especificidade").val("");
            $("#lote").val("");
            $("#dose").val("");
            $("#data_aplicacao").val("");
        }
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
});

function validaCamposVacina() {
    var animal = $("#animal").val();
    if (animal != "" && listaVacinas.length > 0) {
        $("#lista_vacinas").val(JSON.stringify(listaVacinas));
        camposValidosVacina = true;

    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

function removeLinha(obj) {
    var vacinaRemovida = [];
    $(obj).parent().parent().children().each(function() {
        vacinaRemovida.push($(this).text());
    });
    var dataTemp = vacinaRemovida[3].split("/");
    vacinaRemovida[3] = dataTemp[2] + "-" + dataTemp[1] + "-" + dataTemp[0];

    function encontraVacina(elemento) {
        if (elemento.especificidade == vacinaRemovida[0] && elemento.lote == vacinaRemovida[1] &&
            elemento.dose == vacinaRemovida[2] && elemento.data_aplicacao == vacinaRemovida[3]) {
            return true;
        }
        return false;
    }
    var i = listaVacinas.findIndex(encontraVacina);
    if (i != -1) {
        $(obj).parent().parent().remove();
        listaVacinas.splice(i, 1);
        if (listaVacinas.length == 0) {
            $("#tabela_vacinas tbody").html(`
                <tr>
                    <td colspan="5">Não há vacinas inseridas.</td>
                </tr>
            `);
        }
    } else {
        alert("Erro ao remover a vacina!");
    }
    console.log(listaVacinas);
}

$(document).ready(function() {
    $('#form_vacina').submit(function(event) {
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
    listaVacs = listaTasks;

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
                    mensagem = "Vacina cadastrada com sucesso!";
                } else if (taskResult == "ERRO_DADOS") {
                    mensagem = "Erro no salvamento dos dados!";
                } else if (taskResult == "ERRO_BLOCKCHAIN") {
                    mensagem = "Erro ao salvar o dado na blockchain!";
                } else {
                    mensagem = "Erro interno durante a tarefa assíncrona!";
                }
                check += 1;
                for (let i = 0; i < listaVacs.length; i++) {
                    if (res.task_id == listaVacs[i].task_id) {
                        mensagens.push({
                            "id_vacina": listaVacs[i].id_vacina,
                            "mensagem": mensagem
                        })
                    }
                }
                if (check == listaVacs.length - listaExistentes.length) {
                    $(".loader").toggle();
                    const quebraLinha = "\r\n";
                    var msg = "";
                    for (let i = 0; i < mensagens.length; i++) {
                        msg += `Vacina ${mensagens[i].id_vacina+1}: ${mensagens[i].mensagem}`;
                        msg += quebraLinha;
                    }
                    for (let i = 0; i < listaExistentes.length; i++) {
                        msg += `Vacina ${listaExistentes[i].id_vacina+1}: Vacina já cadastrada para esse animal`;
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