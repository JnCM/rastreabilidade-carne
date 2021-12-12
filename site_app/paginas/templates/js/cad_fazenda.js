var camposValidosFazenda = false;

$("#salvar").click(function(event){
    event.preventDefault();
    validaCamposFazenda();
    if(camposValidosFazenda){
        $(".loader").toggle();
        $("#form_fazenda").submit();
    }
});

function validaCamposFazenda(){
    var nomeFazenda = $("#nome_fazenda").val();
    var localizacaoFazenda = $("#localizacao_fazenda").val();
    var criacaoExtensiva = $('#criacao_extensiva').is(':checked');
    var criacaoIntensiva = $('#criacao_intensiva').is(':checked');
    if(nomeFazenda != "" && localizacaoFazenda != "" && (criacaoExtensiva || criacaoIntensiva)){
        camposValidosFazenda = true;
    }else{
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event){
    event.preventDefault();
    location.href = "/";
});

$(document).ready(function(){
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

            success: function(result){
                $(".loader").toggle();
                result = JSON.parse(result);
                if(result.resposta == 'OK'){
                    alert("Fazenda cadastrada com sucesso!");
                    location.href = "/";
                }else if(result.resposta == "FAZENDA EXISTENTE"){
                    alert("Fazenda já cadastrada!");
                    $("nome_fazenda").val("");
                    $("localizacao_fazenda").val("");
                }else{
                    alert("Erro interno! Tente novamente mais tarde.");
                }
            },
            fail: function(msg){
                $(".loader").toggle();
                alert("Erro ao salvar!");
            },
            beforeSend: function(){
            },
            complete: function(msg){
            },
            error: function(msg){
                $(".loader").toggle();
                alert("Erro interno!");
            },
            timeout: 180000
        });
        event.preventDefault();
    });
});
