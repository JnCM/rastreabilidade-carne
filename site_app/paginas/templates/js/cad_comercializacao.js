var camposValidosComercializacao = false;
var listaEmbalagens = [];

$("#salvar").click(function(event) {
    event.preventDefault();
    validaCamposComercializacao();
    if (camposValidosComercializacao) {
        $(".loader").toggle();
        $("#form_comercializacao").submit();
    }
});

$("#add_embalagem").click(function(event) {
    event.preventDefault();
    var idEmbalagem = $("#embalagem").val();
    var embalagem = $("#embalagem option:selected").text();
    console.log(idEmbalagem);
    console.log(embalagem);
    var flag = false;
    if (idEmbalagem != "") {
        for (let i = 0; i < listaEmbalagens.length; i++) {
            if (idEmbalagem == listaEmbalagens[i]) {
                flag = true;
                break
            }
        }
        if (flag) {
            alert("Embalagem já inserida para cadastro!");
        } else {
            if (listaEmbalagens.length == 0) {
                $("#tabela_comercializacao tbody").html("");
            }
            $("#tabela_comercializacao tbody").append(`
                <tr id="${idEmbalagem}">
                    <td scope="col" style="font-size: 20px">${embalagem}</td>
                    <td scope="col"><button class="btn btn-danger" style="border-radius: 2rem; margin-top: 5%;" onclick="removeLinhaTabComercializacao(this)"><i class="fa fa-times-circle"></i></button>
                </tr>
            `);
            listaEmbalagens.push(idEmbalagem);
            $("#modal-comercializacao").modal('hide');
            $('#embalagem').prop('selectedIndex', 0);
        }
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
});

function validaCamposComercializacao() {
    var dataVenda = $("#data_venda").val();

    if (dataVenda != "" && listaEmbalagens.length > 0) {
        $("#lista_embalagens").val(JSON.stringify(listaEmbalagens));
        camposValidosComercializacao = true;
    } else {
        alert("Campo(s) vazio(s) detectado(s)! Por favor, preencha todos os campos.");
    }
}

$("#voltar").click(function(event) {
    event.preventDefault();
    location.href = "/";
});

function removeLinhaTabComercializacao(obj) {
    var embalagemRemovida = $(obj).parent().parent().attr('id');

    function encontraEmbalagem(elemento) {
        if (elemento == embalagemRemovida) {
            return true;
        }
        return false;
    }
    var i = listaEmbalagens.findIndex(encontraEmbalagem);
    if (i != -1) {
        $(obj).parent().parent().remove();
        listaEmbalagens.splice(i, 1);
        if (listaEmbalagens.length == 0) {
            $("#tabela_comercializacao tbody").html(`
                <tr>
                    <td colspan="2">Não há embalagens inseridas.</td>
                </tr>
            `);
        }
    } else {
        alert("Erro ao remover a embalagem!");
    }
    console.log(listaEmbalagens);
}

$(document).ready(function() {
    $('#form_comercializacao').submit(function(event) {
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
                    alert("Comercialização cadastrada com sucesso!");
                    location.href = "/";
                } else if (result.resposta == "COMERCIALIZACAO EXISTENTE") {
                    alert("Embalagem já foi vendida!");
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

window.addEventListener("load", function() {
    var now = new Date();
    var utcString = now.toISOString().substring(0, 19);
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    var localDatetime = year + "-" +
        (month < 10 ? "0" + month.toString() : month) + "-" +
        (day < 10 ? "0" + day.toString() : day) + "T" +
        (hour < 10 ? "0" + hour.toString() : hour) + ":" +
        (minute < 10 ? "0" + minute.toString() : minute);
    var datetimeField = document.getElementById("data_venda");
    datetimeField.value = localDatetime;
});