$("#animal").change(function(event){
    event.preventDefault();
    $(".loader").toggle();
    $.get('/get_embalagens_impressao', {animal: $("#animal").val()}, function(response){
        response = JSON.parse(response);
        if(response.mensagem == "OK"){
            if(response.lista_embalagens.length > 0){
                $("#baixar-todas").prop("disabled", false);
                $("#tabela_embalagens tbody").html("");
                var listaEmbalagens = response.lista_embalagens;
                for (let i = 0; i < listaEmbalagens.length; i++) {
                    var tipoCorteExibido = "";
                    switch (listaEmbalagens[i].tipo_corte) {
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
                            <td scope="col">${listaEmbalagens[i].id_embalagem}</td>
                            <td scope="col">${listaEmbalagens[i].peso_corte}</td>
                            <td scope="col">${tipoCorteExibido}</td>
                            <td scope="col"><button type="button" class="btn btn-success" onclick="window.open('baixar_qrcode?id_embalagem=${listaEmbalagens[i].id_embalagem}')"><i class="fa fa-download" aria-hidden="true"></i></button></td>
                        </tr>
                    `);
                }
            }else{
                $("#tabela_embalagens tbody").html(`
                    <tr>
                        <td colspan="4">Não há embalagens para impressão.</td>
                    </tr>
                `);
                $("#baixar-todas").prop("disabled", true);
            }
        }else{
            alert("Erro interno no servidor! Tente novamente mais tarde.");
            $("#baixar-todas").prop("disabled", true);
        }
        $(".loader").toggle();
    });
});

$("#baixar-todas").click(function(event){
    event.preventDefault();
    window.open(`baixar_todas?id_animal=${$("#animal").val()}`);
});

$("#voltar").click(function(event){
    event.preventDefault();
    location.href = "/";
});
