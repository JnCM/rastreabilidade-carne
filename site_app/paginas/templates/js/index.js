$("#reg_fazenda").click(function(){
    location.href = "/cadastro_fazenda";
});

$("#reg_animal").click(function(){
    location.href = "/cadastro_animal";
});

$("#reg_vacina").click(function(){
    location.href = "/cadastro_vacina";
});

$("#reg_terminacao").click(function(){
    location.href = "/cadastro_terminacao";
});

$("#reg_venda").click(function(){
    location.href = "/cadastro_venda";
});

$("#reg_frigorifico").click(function(){
    location.href = "/cadastro_frigorifico";
});

$("#reg_embalagem").click(function(){
    location.href = "/cadastro_embalagem";
});

$("#reg_abate").click(function(){
    location.href = "/cadastro_abate";
});

$("#reg_qualidade").click(function(){
    location.href = "/cadastro_qualidade";
});

$("#ver_embalagem").click(function(){
    location.href = "/embalagens/" + $("#id_embalagem").val();
});

$("#reg_comercializacao").click(function(){
    location.href = "/cadastro_comercializacao";
});

$("#imprime_qrcodes").click(function(){
    location.href = "/imprimir_qrcodes";
});
