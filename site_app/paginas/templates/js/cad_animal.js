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
                $(".loader").toggle();
                result = JSON.parse(result);
                if (result.resposta == 'OK') {
                    alert("Animal cadastrado com sucesso!");
                    location.href = "/";
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