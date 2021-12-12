from django.db import models

class Fazenda(models.Model):
    # ID da fazenda
    id_fazenda = models.IntegerField(primary_key=True)
    # Nome da fazenda
    nome_fazenda = models.CharField(max_length=255)
    # Localizacao da fazenda
    localizacao_fazenda = models.TextField()
    # Tipo de criacao (E = Extensiva / I = Intensiva)
    tipo_criacao = models.CharField(max_length=2)

    class Meta:
        db_table = u'tb_fazenda'


class Animal(models.Model):
    # ID do animal (Numero SISBOV)
    id_animal = models.CharField(primary_key=True, max_length=15)
    # Raca do animal
    raca = models.CharField(max_length=255)
    # Genero do animal (M = Macho / F = Femea)
    genero = models.CharField(max_length=2)
    # Data de nascimento do animal
    data_nascimento = models.DateField()
    # Peso do animal ao nascer (kg)
    peso_nascimento = models.FloatField()
    # ID da fazenda responsavel pelo animal
    id_fazenda = models.IntegerField()

    class Meta:
        db_table = u'tb_animal'


class Vacina(models.Model):
    # Identificador da vacina
    id_vacina = models.IntegerField(primary_key=True)
    # Especificidade da vacina
    especificidade = models.CharField(max_length=255)
    # Lote da vacina
    lote = models.CharField(max_length=255)
    # Dose da vacina (mL)
    dose = models.FloatField()
    # Data da aplicacao da vacina
    data_aplicacao = models.DateField()
    # Identificador do animal que tomou a vacina
    id_animal = models.CharField(max_length=15)

    class Meta:
        db_table = u'tb_vacina'


class Terminacao(models.Model):
    # Identificador da terminacao
    id_terminacao = models.IntegerField(primary_key=True)
    # Data de inicio da terminacao
    data_inicio = models.DateField()
    # Idade do animal ao entrar na terminacao
    idade_animal = models.IntegerField()
    # Peso do animal no inicio da terminacao (kg)
    peso_inicial = models.FloatField()
    # Se o animal e castrado ou nao (S = Sim / N = Nao)
    animal_castrado = models.CharField(max_length=2)
    # Sistema de terminacao (P = Pasto / C = Confinamento)
    sistema_terminacao = models.CharField(max_length=2)
    # Identificador do animal associado a terminacao
    id_animal = models.CharField(max_length=15)

    class Meta:
        db_table = u'tb_terminacao'


class Venda(models.Model):
    # Identificador da venda
    id_venda = models.IntegerField(primary_key=True)
    # Data da venda
    data_venda = models.DateField()
    # Frigorifico que comprou o animal
    frigorifico_comprador = models.IntegerField()
    
    class Meta:
        db_table = u'tb_venda'


class VendaAnimal(models.Model):
    # Identificador de um item de uma venda
    id_item = models.IntegerField(primary_key=True)
    # Identificador da venda realizada
    id_venda = models.IntegerField()
    # Peso final do animal
    peso_final = models.FloatField()
    # ITU mínimo
    itu_min = models.FloatField()
    # ITU medio
    itu_medio = models.FloatField()
    # ITU máximo
    itu_max = models.FloatField()
    # Identificador do animal vendido
    id_animal = models.CharField(max_length=15)

    class Meta:
        db_table = u'tb_venda_animal'


class Frigorifico(models.Model):
    # Identificador do frigorifico
    id_frigorifico = models.IntegerField(primary_key=True)
    # Nome do frigorifico
    nome_frigorifico = models.CharField(max_length=255)
    # Localizacao do frigorifico
    localizacao_frigorifico = models.TextField()
    # CNPJ do frigorifico
    cnpj = models.CharField(max_length=15)
    # Responsavel pelo frigorifico
    responsavel = models.CharField(max_length=255)

    class Meta:
        db_table = u'tb_frigorifico'


class Abate(models.Model):
    # Identificador do abate
    id_abate = models.IntegerField(primary_key=True)
    # Data do abate
    data_abate = models.DateField()
    # PH inicial
    ph_inicial = models.FloatField()
    # PH final
    ph_final = models.FloatField()
    # Gordura subcutanea
    gordura_subcutanea = models.FloatField()
    # Peso da carcaca quente na direita
    peso_carcaca_quente_direita = models.FloatField()
    # Peso da carcaca quente na esquerda
    peso_carcaca_quente_esquerda = models.FloatField()
    # Peso da carcaca frio na direita
    peso_carcaca_frio_direita = models.FloatField()
    # Peso da carcaca frio na esquerda
    peso_carcaca_frio_esquerda = models.FloatField()
    # Identificador da animal
    id_animal = models.CharField(max_length=45)

    class Meta:
        db_table = u'tb_abate'


class Qualidade(models.Model):
    # Identificador da qualidade
    id_qualidade = models.IntegerField(primary_key=True)
    # Comprimento do sarcomero
    comprimento_sarcomero = models.FloatField()
    # Forca do cisalhamento
    forca_cisalhamento = models.FloatField()
    # Perda por descongelamento
    perda_descongelamento = models.FloatField()
    # Perda por coccao
    perda_coccao = models.FloatField()
    # Cor da carne L
    cor_carne_l = models.CharField(max_length=45)
    # Cor da carne A
    cor_carne_a = models.CharField(max_length=45)
    # Cor da carne B
    cor_carne_b = models.CharField(max_length=45)
    # Cor da gordura L
    cor_gordura_l = models.CharField(max_length=45)
    # Cor da gordura A
    cor_gordura_a = models.CharField(max_length=45)
    # Cor da gordura B
    cor_gordura_b = models.CharField(max_length=45)
    # Identificador do animal
    id_animal = models.CharField(max_length=15)

    class Meta:
        db_table = u'tb_qualidade'


class Embalagem(models.Model):
    # Identificador da embalagem
    id_embalagem = models.IntegerField(primary_key=True)
    # Data da embalagem
    data_embalagem = models.DateField()
    # Tipo do corte da carne
    tipo_corte = models.CharField(max_length=3)
    # Peso do corte da carne
    peso_corte = models.FloatField()
    # Identificador do animal
    id_animal = models.CharField(max_length=15)

    class Meta:
        db_table = u'tb_embalagem'


class Comercializacao(models.Model):
    # Identificador da comercialização
    id_comercializacao = models.IntegerField(primary_key=True)
    # Data de saída da embalagem
    data_venda = models.DateTimeField()
    
    class Meta:
        db_table = u'tb_comercializacao'


class ComercializacaoEmbalagem(models.Model):
    # Identificador do item da comercialização
    id_item = models.IntegerField(primary_key=True)
    # Identificador da embalagem vendida
    id_embalagem = models.IntegerField()
    # Identificador da comercializacao
    id_comercializacao = models.IntegerField()

    class Meta:
        db_table = u'tb_comercializacao_embalagem'


class Tabela(models.Model):
    # Identificador da tabela do banco
    id_tabela = models.IntegerField(primary_key=True)
    # Nome da tabela
    nome_tabela = models.CharField(max_length=50)

    class Meta:
        db_table = u'tb_tabela'


class Hash(models.Model):
    # Identificador padrão
    id_hash = models.IntegerField(primary_key=True)
    # Identificador de qual tabela o item pertence
    id_tabela = models.IntegerField()
    # Identificador do item
    id_item = models.IntegerField()
    # Identificador do item na blockchain
    id_hash_blockchain = models.IntegerField()

    class Meta:
        db_table = u'tb_hash'


class Qrcode(models.Model):
    # Identificador padrão
    id_qrcode = models.IntegerField(primary_key=True)
    # Nome da Imagem
    nome_imagem = models.CharField(max_length=50)
    # Binário da imagem
    binario_imagem = models.BinaryField(max_length=10240)
    # Identificador da embalagem
    id_embalagem = models.IntegerField()

    class Meta:
        db_table = u'tb_qrcode'
