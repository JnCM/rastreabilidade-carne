var camposValidosVenda = false;
var listaVendas = [];
var listaItens = [];
var listaExistentes = [];
var check = 0;
var mensagens = [];

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposVenda();
    if (camposValidosVenda) {
        $(".loader").toggle();
        $("#form_venda").submit();
    }
});

$("#add_venda").click(function(event) {
    event.preventDefault();
    var animal = $("#animal").val();
    var pesoFinal = $("#peso_final").val();
    var ituMedio = $("#itu_medio").val();
    var ituMin = $("#itu_min").val();
    var ituMax = $("#itu_max").val();
    var flag = false;
    if (animal != "" && pesoFinal != "" && ituMedio != "" && ituMax != "" && ituMin != "") {
        for (let i = 0; i < listaVendas.length; i++) {
            if (animal == listaVendas[i].animal) {
                flag = true;
                break
            }
        }
        if (flag) {
            alert("Animal já inserido para a venda!");
        } else {
            if (listaVendas.length == 0) {
                $("#tabela_vendas tbody").html("");
            }
            var venda = {
                "animal": animal,
                "peso_final": pesoFinal,
                "itu_medio": ituMedio,
                "itu_max": ituMax,
                "itu_min": ituMin
            };
            $("#tabela_vendas tbody").append(`
                <tr>
                    <td scope="col" style="vertical-align: middle;">${venda.animal}</td>
                    <td scope="col" style="vertical-align: middle;">${venda.peso_final}</td>
                    <td scope="col" style="vertical-align: middle;">${venda.itu_min}</td>
                    <td scope="col" style="vertical-align: middle;">${venda.itu_medio}</td>
                    <td scope="col" style="vertical-align: middle;">${venda.itu_max}</td>
                    <td scope="col" style="vertical-align: middle;"><button class="btn btn-danger" style="border-radius: 2rem;" onclick="removeLinhaTabVenda(this)"><i class="fa fa-times-circle"></i></button>
                </tr>
            `);
            listaVendas.push(venda);
            $("#modal-venda").modal('hide');
            $("#animal").val("");
            $("#peso_final").val("");
            $("#itu_medio").val("");
        }
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
});

function validaCamposVenda() {
    var idFrigorifico = $("#frigorifico").val();
    var dataVenda = $("#data_venda").val();
    if (idFrigorifico != "" && dataVenda != "" && listaVendas.length > 0) {
        $("#lista_vendas").val(JSON.stringify(listaVendas));
        camposValidosVenda = true;
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

function removeLinhaTabVenda(obj) {
    var vendaRemovida = [];
    $(obj).parent().parent().children().each(function() {
        vendaRemovida.push($(this).text());
    });

    function encontraVenda(elemento) {
        if (elemento.animal == vendaRemovida[0]) {
            return true;
        }
        return false;
    }
    var i = listaVendas.findIndex(encontraVenda);
    if (i != -1) {
        $(obj).parent().parent().remove();
        listaVendas.splice(i, 1);
        if (listaVendas.length == 0) {
            $("#tabela_vendas tbody").html(`
                <tr>
                    <td colspan="4">Não há animais inseridos.</td>
                </tr>
            `);
        }
    } else {
        alert("Erro ao remover o item da venda!");
    }
    console.log(listaVendas);
}

$(document).ready(function() {
    $('#form_venda').submit(function(event) {
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
                    getStatusVenda(result.task_id_venda);
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
    listaItens = listaTasks;

    for (let i = 0; i < listaTasks.length; i++) {
        if (listaTasks[i].task_id != -1) {
            getStatus(listaTasks[i].task_id);
        } else {
            listaExistentes.push(listaTasks[i]);
        }
    }
}

function getStatusVenda(taskID) {
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
                    alert("Venda cadastrada com sucesso!");
                } else if (taskResult == "ERRO_DADOS") {
                    alert("Erro no salvamento dos dados da venda!");
                } else if (taskResult == "ERRO_BLOCKCHAIN") {
                    alert("Erro ao salvar o dado da venda na blockchain!");
                } else {
                    alert("Erro interno durante a tarefa assíncrona da venda!");
                }
            } else {
                setTimeout(function() {
                    getStatusVenda(res.task_id);
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
                    mensagem = "Animal vendido com sucesso!";
                } else if (taskResult == "ERRO_DADOS") {
                    mensagem = "Erro no salvamento dos dados!";
                } else if (taskResult == "ERRO_BLOCKCHAIN") {
                    mensagem = "Erro ao salvar o dado na blockchain!";
                } else {
                    mensagem = "Erro interno durante a tarefa assíncrona!";
                }
                check += 1;
                for (let i = 0; i < listaItens.length; i++) {
                    if (res.task_id == listaItens[i].task_id) {
                        mensagens.push({
                            "id_item_venda": listaItens[i].id_item_venda,
                            "mensagem": mensagem
                        })
                    }
                }
                if (check == listaItens.length - listaExistentes.length) {
                    $(".loader").toggle();
                    const quebraLinha = "\r\n";
                    var msg = "";
                    for (let i = 0; i < mensagens.length; i++) {
                        msg += `Animal ${mensagens[i].id_item_venda+1}: ${mensagens[i].mensagem}`;
                        msg += quebraLinha;
                    }
                    for (let i = 0; i < listaExistentes.length; i++) {
                        msg += `Animal ${listaExistentes[i].id_item_venda+1}: Animal já foi vendido`;
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

$("#data_venda, #frigorifico").change(function(event) {
    event.preventDefault();
    if ($("#data_venda").val() != "" && $("#frigorifico").val() != "") {
        $("#add_animal").prop("disabled", false);
    } else {
        $("#add_animal").prop("disabled", true);
    }
});

$("#animal").change(function(event) {
    event.preventDefault();
    if ($("#animal").val() != "") {
        $(".loader").toggle();
        $.get('/get_itu_medio', { animal: $("#animal").val(), data_venda: $("#data_venda").val() }, function(response) {
            response = JSON.parse(response);
            if (response.mensagem == "OK") {
                var ituMedio = response.itu_medio;
                var ituMax = response.itu_min;
                var ituMin = response.itu_max;
                $("#itu_medio").val(ituMedio);
                $("#itu_max").val(ituMax);
                $("#itu_min").val(ituMin);
            } else {
                alert("Erro interno no servidor! Tente novamente mais tarde.")
            }
            $(".loader").toggle();
        });
    }
});