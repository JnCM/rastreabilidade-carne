var camposValidosTerminacao = false;

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposTerminacao();
    if (camposValidosTerminacao) {
        $(".loader").toggle();
        $("#form_terminacao").submit();
    }
});

function validaCamposTerminacao() {
    var idAnimal = $("#animal").val();
    var dataInicio = $("#data_inicio").val();
    var idadeAnimal = $("#idade_animal").val();
    var pesoInicial = $("#peso_inicial").val();
    var castradoSim = $('#sim').is(':checked');
    var castradoNao = $('#nao').is(':checked');
    var sistemaPasto = $('#pasto').is(':checked');
    var sistemaConfinamento = $('#confinamento').is(':checked');
    if (idAnimal != "" && dataInicio != "" && idadeAnimal != "" && pesoInicial != "" &&
        (castradoSim || castradoNao) && (sistemaPasto || sistemaConfinamento)) {

        camposValidosTerminacao = true;

    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

$(document).ready(function() {
    $('#form_terminacao').submit(function(event) {
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
                $(".loader").toggle();
                result = JSON.parse(result);
                if (result.resposta == 'OK') {
                    alert("Terminação cadastrada com sucesso!");
                    location.href = "/";
                } else if (result.resposta == "TERMINACAO EXISTENTE") {
                    alert("Animal já cadastrado a uma terminação!");
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