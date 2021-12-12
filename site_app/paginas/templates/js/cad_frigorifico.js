var camposValidosFrigorifico = false;

$("#cnpj").mask("99.999.999/9999-99");

$("#salvar").click(function(event){
    event.preventDefault();
    validaCamposFrigorifico();
    if(camposValidosFrigorifico){
        $(".loader").toggle();
        $("#form_frigorifico").submit();
    }
});

function validaCamposFrigorifico(){
    var nomeFrigorifico = $("#nome_frigorifico").val();
    var localizacaoFrigorifico = $("#localizacao_frigorifico").val();
    var cnpj = $("#cnpj").val();
    var responsavel = $("#responsavel").val();
    if(nomeFrigorifico != "" && localizacaoFrigorifico != "" && responsavel != "" && cnpj != ""){
        camposValidosFrigorifico = true;
    }else{
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
    // if(!validarCNPJ(cnpj)){
    //     alert("CNPJ inválido!");
    //     $("#cnpj").val("");
    // }else if(nomeFrigorifico != "" && localizacaoFrigorifico != "" && responsavel != ""){
    //     camposValidosFrigorifico = true;
    // }else{
    //     alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    // }
}

function validarCNPJ(cnpj) {
 
    cnpj = cnpj.replace(/[^\d]+/g,'');
 
    if(cnpj == '') return false;
     
    if (cnpj.length != 14)
        return false;
 
    // Elimina CNPJs invalidos conhecidos
    if (cnpj == "00000000000000" || 
        cnpj == "11111111111111" || 
        cnpj == "22222222222222" || 
        cnpj == "33333333333333" || 
        cnpj == "44444444444444" || 
        cnpj == "55555555555555" || 
        cnpj == "66666666666666" || 
        cnpj == "77777777777777" || 
        cnpj == "88888888888888" || 
        cnpj == "99999999999999")
        return false;
         
    // Valida DVs
    tamanho = cnpj.length - 2
    numeros = cnpj.substring(0,tamanho);
    digitos = cnpj.substring(tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0))
        return false;
         
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0,tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1))
          return false;
           
    return true;
    
}

$("#voltar").click(function(event){
    event.preventDefault();
    location.href = "/";
});

$(document).ready(function(){
    $('#form_frigorifico').submit(function(event) {
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
                    alert("Frigorífico cadastrado com sucesso!");
                    location.href = "/";
                }else if(result.resposta == "FRIGORIFICO EXISTENTE"){
                    alert("Frigorífico já cadastrado!");
                    $("#nome_frigorifico").val("");
                    $("#localizacao_frigorifico").val("");
                    $("#cnpj").val("");
                    $("#responsavel").val("");
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
