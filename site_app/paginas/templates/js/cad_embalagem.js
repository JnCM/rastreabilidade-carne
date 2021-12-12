var camposValidosEmbalagem = false;
var listaEmbalagens = [];

$("#salvar").click(function(event){
    event.preventDefault();
    validaCamposEmbalagem();
    if(camposValidosEmbalagem){
        $(".loader").toggle();
        $("#form_embalagem").submit();
    }
});

$("#add_embalagem").click(function(event){
    event.preventDefault();
    var pesoCorte = $("#peso_corte").val();
    var tipoCorte = $("input[name=tipo_corte]:checked").val();
    var flag = false;
    if(pesoCorte != "" && tipoCorte != ""){
        for (let i = 0; i < listaEmbalagens.length; i++) {
            if(pesoCorte == listaEmbalagens[i].peso_corte && tipoCorte == listaEmbalagens[i].tipo_corte){
                flag = true;
                break
            }
        }
        if(flag){
            alert("Embalagem já inserida para cadastro!");
        }else{
            if(listaEmbalagens.length == 0){
                $("#tabela_embalagens tbody").html("");
            }
            var embalagem = {
                "peso_corte": pesoCorte,
                "tipo_corte": tipoCorte
            };
            var tipoCorteExibido = "";
            switch (tipoCorte) {
                case "CF":
                    tipoCorteExibido = "Contrafilé";
                    break;
                case "FR":
                    tipoCorteExibido = "Fraldinha";
                    break;
                case "FM":
                    tipoCorteExibido = "Filé-mignon";
                    break;
                case "PC":
                    tipoCorteExibido = "Picanha";
                default:
                    break;
            }
            $("#tabela_embalagens tbody").append(`
                <tr>
                    <td scope="col">${embalagem.peso_corte}</td>
                    <td scope="col">${tipoCorteExibido}</td>
                    <td scope="col"><button class="btn btn-danger" style="border-radius: 2rem;" onclick="removeLinhaTabEmbalagem(this)"><i class="fa fa-times-circle"></i></button>
                </tr>
            `);
            listaEmbalagens.push(embalagem);
            $("#modal-embalagem").modal('hide');
            $("#peso_corte").val("");
            $("#tipo_corte").val("");
        }
    }else{
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
});

function validaCamposEmbalagem(){
    var idAnimal = $("#animal").val();
    var dataEmbalagem = $("#data_embalagem").val();
    if(idAnimal != "" && dataEmbalagem != "" && listaEmbalagens.length > 0){
        $("#lista_embalagens").val(JSON.stringify(listaEmbalagens));
        camposValidosEmbalagem = true;
    
    }else{
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event){
    event.preventDefault();
    location.href = "/";
});

function removeLinhaTabEmbalagem(obj){
    var embalagemRemovida = [];
    $(obj).parent().parent().children().each(function(){
        embalagemRemovida.push($(this).text());
    });
    var tipoCorte = "";
    switch (embalagemRemovida[1]) {
        case "Contrafilé":
            tipoCorte = "CF";
            break;
        case "Fraldinha":
            tipoCorte = "FR";
            break;
        case "Filé-mignon":
            tipoCorte = "FM";
            break;
        case "Picanha":
            tipoCorte = "PC";
        default:
            break;
    }
    function encontraEmbalagem(elemento){
        if(elemento.peso_corte == embalagemRemovida[0] && elemento.tipo_corte == tipoCorte){
            return true;
        }
        return false;
    }
    var i = listaEmbalagens.findIndex(encontraEmbalagem);
    if(i != -1){
        $(obj).parent().parent().remove();
        listaEmbalagens.splice(i,1);
        if(listaEmbalagens.length == 0){
            $("#tabela_embalagens tbody").html(`
                <tr>
                    <td colspan="3">Não há embalagens inseridas.</td>
                </tr>
            `);
        }
    }else{
        alert("Erro ao remover a embalagem!");
    }
    console.log(listaEmbalagens);
}

$(document).ready(function(){
    $('#form_embalagem').submit(function(event) {
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
                    alert("Embalagem cadastrada com sucesso!");
                    location.href = "/";
                }else if(result.resposta == "EMBALAGEM EXISTENTE"){
                    alert("Animal já cadastrado a uma embalagem!");
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
