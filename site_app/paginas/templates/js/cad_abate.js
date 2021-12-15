var camposValidosAbate = false;

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposAbate();
    if (camposValidosAbate) {
        $(".loader").toggle();
        $("#form_abate").submit();
    }
});

function validaCamposAbate() {
    var idAnimal = $("#animal").val();
    var dataAbate = $("#data_abate").val();
    var phInicial = $("#ph_inicial").val();
    var phFinal = $("#ph_final").val();
    var gordura = $("#gordura_subcutanea").val();
    var pesoQuenteE = $("#peso_carcaca_quente_esquerda").val();
    var pesoQuenteD = $("#peso_carcaca_quente_direita").val();
    var pesoFrioE = $("#peso_carcaca_frio_esquerda").val();
    var pesoFrioD = $("#peso_carcaca_frio_direita").val();

    if (idAnimal != "" && dataAbate != "" && phInicial != "" && phFinal != "" && gordura != "" &&
        pesoQuenteE != "" && pesoQuenteD != "" && pesoFrioE != "" && pesoFrioD != "") {

        camposValidosAbate = true;

    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

$(document).ready(function() {
    $('#form_abate').submit(function(event) {
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
                } else if (result.resposta == "ABATE EXISTENTE") {
                    alert("Animal já cadastrado a um abate!");
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
                    alert("Abate cadastrado com sucesso!");
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