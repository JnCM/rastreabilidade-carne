var camposValidosComercializacao = false;
var listaEmbalagens = [];
var listaEmbs = [];
var listaExistentes = [];
var check = 0;
var mensagens = [];

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposComercializacao();
    if (camposValidosComercializacao) {
        $(".loader").toggle();
        $("#form_comercializacao").submit();
    }
});

$("#add_embalagem").click(function(event) {
    event.preventDefault();
    var idEmbalagem = $("#embalagem").val();
    var embalagem = $("#embalagem option:selected").text();
    console.log(idEmbalagem);
    console.log(embalagem);
    var flag = false;
    if (idEmbalagem != "") {
        for (let i = 0; i < listaEmbalagens.length; i++) {
            if (idEmbalagem == listaEmbalagens[i]) {
                flag = true;
                break
            }
        }
        if (flag) {
            alert("Embalagem já inserida para cadastro!");
        } else {
            if (listaEmbalagens.length == 0) {
                $("#tabela_comercializacao tbody").html("");
            }
            $("#tabela_comercializacao tbody").append(`
                <tr id="${idEmbalagem}">
                    <td scope="col" style="font-size: 20px">${embalagem}</td>
                    <td scope="col"><button class="btn btn-danger" style="border-radius: 2rem; margin-top: 5%;" onclick="removeLinhaTabComercializacao(this)"><i class="fa fa-times-circle"></i></button>
                </tr>
            `);
            listaEmbalagens.push(idEmbalagem);
            $("#modal-comercializacao").modal('hide');
            $('#embalagem').prop('selectedIndex', 0);
        }
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
});

function validaCamposComercializacao() {
    var dataVenda = $("#data_venda").val();

    if (dataVenda != "" && listaEmbalagens.length > 0) {
        $("#lista_embalagens").val(JSON.stringify(listaEmbalagens));
        camposValidosComercializacao = true;
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

function removeLinhaTabComercializacao(obj) {
    var embalagemRemovida = $(obj).parent().parent().attr('id');

    function encontraEmbalagem(elemento) {
        if (elemento == embalagemRemovida) {
            return true;
        }
        return false;
    }
    var i = listaEmbalagens.findIndex(encontraEmbalagem);
    if (i != -1) {
        $(obj).parent().parent().remove();
        listaEmbalagens.splice(i, 1);
        if (listaEmbalagens.length == 0) {
            $("#tabela_comercializacao tbody").html(`
                <tr>
                    <td colspan="2">Não há embalagens inseridas.</td>
                </tr>
            `);
        }
    } else {
        alert("Erro ao remover a embalagem!");
    }
    console.log(listaEmbalagens);
}

$(document).ready(function() {
    $('#form_comercializacao').submit(function(event) {
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
                    getStatusComercializacao(result.task_id_comercializacao);
                    verificaStatusTasks(result.tasks_ids);
                } else {
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

function getStatusComercializacao(taskID) {
    $.ajax({
            url: `/tasks/${taskID}/`,
            method: 'GET'
        })
        .done((res) => {
            const taskStatus = res.task_status;

            if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') {
                const taskResult = res.task_result;
                console.log(taskResult);
                if (taskResult == "OK") {
                    alert("Comercialização cadastrada com sucesso!");
                } else if (taskResult == "ERRO_DADOS") {
                    alert("Erro no salvamento dos dados da comercialização!");
                } else if (taskResult == "ERRO_BLOCKCHAIN") {
                    alert("Erro ao salvar o dado da comercialização na blockchain!");
                } else {
                    alert("Erro interno durante a tarefa assíncrona da comercialização!");
                }
            } else {
                setTimeout(function() {
                    getStatusComercializacao(res.task_id);
                }, 1000);
            }
        })
        .fail((err) => {
            $(".loader").toggle();
            console.log(err);
            alert("Erro interno!");
        });
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
                    mensagem = "Embalagem vendida com sucesso!";
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
                        msg += `Embalagem ${listaExistentes[i].id_embalagem+1}: Embalagem já foi vendida`;
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

window.addEventListener("load", function() {
    var now = new Date();
    var utcString = now.toISOString().substring(0, 19);
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    var localDatetime = year + "-" +
        (month < 10 ? "0" + month.toString() : month) + "-" +
        (day < 10 ? "0" + day.toString() : day) + "T" +
        (hour < 10 ? "0" + hour.toString() : hour) + ":" +
        (minute < 10 ? "0" + minute.toString() : minute);
    var datetimeField = document.getElementById("data_venda");
    datetimeField.value = localDatetime;
});