var camposValidosLogin = false;

$("#login").click(function(event){
    event.preventDefault();
    validaCamposLogin();
    if(camposValidosLogin){
        $(".loader").toggle();
        $("#form_login").submit();
    }
});

function validaCamposLogin(){
    var username = $("#username").val();
    var password = $("#password").val();
    if(username != "" && password != ""){
        camposValidosLogin = true;
    }else{
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$(document).ready(function(){
    $('#form_login').submit(function(event) {
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
                if(result.mensagem == 'OK'){
                    location.href = "/";
                }else{
                    alert("Usuário e/ou senha inválidos!");
                }
            },
            fail: function(msg){
                $(".loader").toggle();
                alert("Erro interno! Tente novamente mais tarde.");
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
