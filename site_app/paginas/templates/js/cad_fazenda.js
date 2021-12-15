var camposValidosFazenda = false;

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposFazenda();
    if (camposValidosFazenda) {
        $(".loader").toggle();
        $("#form_fazenda").submit();
    }
});

function validaCamposFazenda() {
    var nomeFazenda = $("#nome_fazenda").val();
    var localizacaoFazenda = $("#localizacao_fazenda").val();
    var criacaoExtensiva = $('#criacao_extensiva').is(':checked');
    var criacaoIntensiva = $('#criacao_intensiva').is(':checked');
    if (nomeFazenda != "" && localizacaoFazenda != "" && (criacaoExtensiva || criacaoIntensiva)) {
        camposValidosFazenda = true;
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

$(document).ready(function() {
    $('#form_fazenda').submit(function(event) {
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
                    getStatus(result.task_id);
                } else if (result.resposta == "FAZENDA EXISTENTE") {
                    alert("Fazenda já cadastrada!");
                    $("nome_fazenda").val("");
                    $("localizacao_fazenda").val("");
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

function getStatus(taskID) {
    $.ajax({
            url: `/tasks/${taskID}/`,
            method: 'GET'
        })
        .done((res) => {
            const taskStatus = res.task_status;

            if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') {
                $(".loader").toggle();
                const taskResult = res.task_result;
                console.log(taskResult);
                if (taskResult == "OK") {
                    alert("Fazenda cadastrada com sucesso!");
                    location.href = "/";
                } else if (taskResult == "ERRO_DADOS") {
                    alert("Erro no salvamento dos dados!");
                } else if (taskResult == "ERRO_BLOCKCHAIN") {
                    alert("Erro ao salvar o dado na blockchain!");
                } else {
                    alert("Erro interno durante a tarefa assíncrona!");
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