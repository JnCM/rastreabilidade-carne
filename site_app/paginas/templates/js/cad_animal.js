var camposValidosAnimal = false;

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposAnimal();
    if (camposValidosAnimal) {
        $(".loader").toggle();
        $("#form_animal").submit();
    }
});

function validaCamposAnimal() {
    var fazenda = $("#fazenda").val();
    var idAnimal = $("#id_animal").val();
    var racaAnimal = $("#raca_animal").val();
    var dataNascimento = $("#data_nascimento").val();
    var pesoNascimento = $("#peso_nascimento").val();
    var generoMacho = $('#macho').is(':checked');
    var generoFemea = $('#femea').is(':checked');
    if (fazenda != "" && idAnimal != "" && idAnimal.length == 15 && racaAnimal != "" && dataNascimento != "" &&
        pesoNascimento != "" && (generoMacho || generoFemea)) {

        camposValidosAnimal = true;

    } else if (idAnimal != "" && idAnimal.length < 15) {
        alert("Nº SISBOV inválido!");
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

$(document).ready(function() {
    $('#form_animal').submit(function(event) {
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
                } else if (result.resposta == "ANIMAL EXISTENTE") {
                    alert("Animal já cadastrado!");
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
                    alert("Animal cadastrado com sucesso!");
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