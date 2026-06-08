from DataBase.databaseConfig import cursor, conn

#TIME 8
cursor.execute('''
INSERT INTO Personagens (
    IdTipoPersonagem,
    IdCla,
    IdArcoAparicao,
    IdOcupacaoClassico,
    IdOcupacaoShippuden,
    IdVila,
    Nome,
    Sobrenome,
    IdadeClasico,
    IdadeShippuden,
    Sexo,
    DataNascimento,
    AlturaClassico,
    AlturaShippuden,
    CorCabelo,
    CorOlhos,
    CorPele,
    DescricaoRoupaClassico,
    DescricaoRoupaShippuden,
    MissoesCompletas,
    Descricao,
    HistoriaPersonagem,
    Estado
)
VALUES

-- KURENAI YUHI

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Terciario'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Kurenai',
    'Yuhi',
    27,
    30,
    'Feminino',
    '1975-06-11',
    1.69,
    1.69,
    'Preto',
    'Vermelho',
    'Clara',
    'Vestido vermelho com mangas longas e padrao circular branco, sandalias ninja e bandana na testa',
    'Roupa semelhante ao classico, porem com jaqueta de jounin verde por cima.',
    697,
    'Lider do Time 8 e especialista em genjutsu.',
    'Kurenai Yuhi e uma kunoichi de elite da Vila da Folha, reconhecida por sua grande habilidade em genjutsu. Tornou-se lider do Time 8, treinando Hinata, Kiba e Shino. Durante a invasao de Pain, estava gravida de Asuma Sarutobi.',
    'Vivo'
),

-- KIBA INUZUKA
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Inuzuka'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Kiba',
    'Inuzuka',
    12,
    16,
    'Masculino',
    '1987-07-07',
    1.52,
    1.69,
    'Castanho',
    'Castanho',
    'Clara',
    'Casaco cinza com capuz de pelo, pintura vermelha nas bochechas e bandana na testa.',
    'Casaco preto com capuz de pelo maior, roupas mais escuras e marcacoes vermelhas mais destacadas no rosto.',
    50,
    'Membro do cla Inuzuka que luta ao lado de seu companheiro Akamaru.',
    'Kiba pertence ao cla Inuzuka, especializado em combate conjunto com caes ninjas. Desde jovem treinou ao lado de Akamaru, desenvolvendo tecnicas combinadas e um olfato extremamente apurado.',
    'Vivo'
),

-- HINATA HYUGA
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Hyuga'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Hinata',
    'Hyuga',
    12,
    16,
    'Feminino',
    '1988-12-27',
    1.47,
    1.60,
    'Azul Escuro',
    'Branco',
    'Clara',
    'Jaqueta creme com detalhes lilas, calca azul escura e bandana no pescoco.',
    'Casaco lilas com detalhes claros, calca escura e visual mais maduro.',
    33,
    'Herdeira do cla Hyuga e usuaria do Byakugan.',
    'Hinata e membro do cla Hyuga, portadora do Byakugan e treinada nas tecnicas do Punho Gentil. Inicialmente timida e insegura, evolui significativamente ao longo da historia, demonstrando coragem durante a invasao de Pain.',
    'Vivo'
),


-- SHINO ABURAME
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Aburame'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Shino',
    'Aburame',
    12,
    16,
    'Masculino',
    '1987-01-23',
    1.56,
    1.75,
    'Castanho Escuro',
    'Preto',
    'Clara',
    'Casaco alto com gola levantada cobrindo parte do rosto, oculos escuros e roupas largas.',
    'Casaco mais longo e escuro, oculos escuros caracteristicos e visual mais imponente.',
    0,
    'Membro do cla Aburame que utiliza insetos em combate.',
    'Shino pertence ao cla Aburame, que vive em simbiose com insetos especiais alimentados por chakra. E extremamente calmo, estrategico e raramente demonstra emocao.',
    'Vivo'
);
''')

#TIME 10
cursor.execute('''
INSERT INTO Personagens (
    IdTipoPersonagem,
    IdCla,
    IdArcoAparicao,
    IdArcoMorte,
    IdOcupacaoClassico,
    IdOcupacaoShippuden,
    IdVila,
    Nome,
    Sobrenome,
    IdadeClasico,
    IdadeShippuden,
    Sexo,
    DataNascimento,
    AlturaClassico,
    AlturaShippuden,
    CorCabelo,
    CorOlhos,
    CorPele,
    DescricaoRoupaClassico,
    DescricaoRoupaShippuden,
    MissoesCompletas,
    Descricao,
    HistoriaPersonagem,
    Estado
)
VALUES

-- ASUMA SARUTOBI
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Sarutobi'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Supressao da Akatsuki'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Asuma',
    'Sarutobi',
    27,
    31,
    'Masculino',
    '1972-10-18',
    1.90,
    1.90,
    'Castanho Escuro',
    'Preto',
    'Clara',
    'Jaqueta verde de jounin, faixa na cintura, bandana na testa e barba media.',
    'Visual semelhante ao classico, mantendo barba, jaqueta de jounin e bandana na testa.',
    719,
    'Lider do Time 10 e especialista em combate corpo a corpo com laminas de chakra.',
    'Asuma Sarutobi e filho do Terceiro Hokage. Tornou-se jounin de elite e liderou o Time 10. Era membro dos Doze Guardioes Ninja. Foi morto por Hidan durante a Missao de Supressao da Akatsuki.',
    'Morto'
),

-- SHIKAMARU NARA

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Nara'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Shikamaru',
    'Nara',
    12,
    16,
    'Masculino',
    '1987-09-22',
    1.52,
    1.70,
    'Preto',
    'Preto',
    'Clara',
    'Camisa verde clara, calca escura, cabelo preso em rabo alto e bandana no braco.',
    'Colete de chunin, cabelo mais longo preso em rabo alto e bandana no braco.',
    39,
    'Genio estrategista do cla Nara especializado em manipulacao de sombras.',
    'Shikamaru e conhecido por sua inteligencia excepcional e preguica aparente. Tornou-se o primeiro chunin entre sua geracao. Liderou a equipe que vingou a morte de Asuma derrotando Hidan.',
    'Vivo'
),

-- INO YAMANAKA

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Yamanaka'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Ino',
    'Yamanaka',
    12,
    16,
    'Feminino',
    '1987-09-23',
    1.49,
    1.62,
    'Loiro',
    'Azul',
    'Clara',
    'Roupa roxa curta com faixa na cintura, cabelo preso em rabo lateral e bandana na cintura.',
    'Roupa roxa mais longa, visual mais maduro e bandana na cintura.',
    40,
    'Kunoichi do cla Yamanaka especializada em tecnicas mentais.',
    'Ino pertence ao cla Yamanaka, que utiliza tecnicas de transferencia de mente. Inicialmente rival de Sakura, amadureceu ao longo da historia e tornou-se uma ninja de suporte essencial durante a guerra.',
    'Vivo'
),

-- CHOJI AKIMICHI

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Akimichi'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Prologo'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Choji',
    'Akimichi',
    12,
    16,
    'Masculino',
    '1987-05-01',
    1.56,
    1.72,
    'Castanho',
    'Preto',
    'Clara',
    'Roupa verde com simbolo do cla Akimichi, cachecol branco e bandana na testa.',
    'Roupa verde mais escura, armadura leve de combate e bandana na testa.',
    39,
    'Membro do cla Akimichi que utiliza tecnicas de expansao corporal.',
    'Choji e membro do cla Akimichi, que converte calorias em chakra para aumentar o tamanho do corpo. Superou insegurancas e demonstrou grande forca emocional e fisica na luta contra Jirobo.',
    'Vivo'
);
''')

#TIME 9
cursor.execute('''
INSERT INTO Personagens (
    IdTipoPersonagem,
    IdCla,
    IdArcoAparicao,
    IdArcoMorte,
    IdOcupacaoClassico,
    IdOcupacaoShippuden,
    IdVila,
    Nome,
    Sobrenome,
    IdadeClasico,
    IdadeShippuden,
    Sexo,
    DataNascimento,
    AlturaClassico,
    AlturaShippuden,
    CorCabelo,
    CorOlhos,
    CorPele,
    DescricaoRoupaClassico,
    DescricaoRoupaShippuden,
    MissoesCompletas,
    Descricao,
    HistoriaPersonagem,
    Estado
)
VALUES

-- MIGHT GUY

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Might',
    'Guy',
    26,
    30,
    'Masculino',
    '1966-01-01',
    1.84,
    1.84,
    'Preto',
    'Preto',
    'Clara',
    'Macacao verde colado ao corpo, colete de jounin verde, aquecedores laranja nas pernas e bandana na cintura.',
    'Visual semelhante ao classico, mantendo macacao verde e bandana na cintura.',
    788,
    'Jounin especialista em taijutsu e lider do Time 9.',
    'Might Guy e um jounin especializado exclusivamente em taijutsu. Rival eterno de Kakashi Hatake, dedicou sua vida ao treinamento extremo. Durante a guerra, abriu o Oitavo Portao contra Madara.',
    'Vivo'
),

-- ROCK LEE

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Rock',
    'Lee',
    13,
    17,
    'Masculino',
    '1987-11-27',
    1.62,
    1.72,
    'Preto',
    'Preto',
    'Clara',
    'Macacao verde semelhante ao de Guy, aquecedores laranja e bandana na cintura.',
    'Macacao verde ajustado, cabelo ligeiramente mais curto e bandana na cintura.',
    61,
    'Ninja especializado exclusivamente em taijutsu.',
    'Rock Lee nao possui talento para ninjutsu ou genjutsu, dedicando-se exclusivamente ao taijutsu. Treinou sob Might Guy e demonstrou grande determinacao durante o Exame Chunin contra Gaara.',
    'Vivo'
),

-- NEJI HYUGA

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Hyuga'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Quarta Grande Guerra Ninja: Climax'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Neji',
    'Hyuga',
    13,
    17,
    'Masculino',
    '1987-07-03',
    1.59,
    1.72,
    'Castanho Escuro',
    'Branco',
    'Clara',
    'Kimono bege com shorts escuros, cabelo longo solto e bandana na testa.',
    'Roupa branca tradicional do cla Hyuga, cabelo longo preso e bandana na testa.',
    62,
    'Prodigio do cla Hyuga e mestre do Punho Gentil.',
    'Neji era membro da familia secundaria do cla Hyuga. Inicialmente acreditava no destino imutavel, mas mudou sua visao apos lutar contra Naruto. Morreu protegendo Hinata e Naruto durante a Quarta Guerra Ninja.',
    'Morto'
),

-- TENTEN

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Chunin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Tenten',
    NULL,
    13,
    17,
    'Feminino',
    '1987-03-09',
    1.54,
    1.64,
    'Castanho',
    'Castanho',
    'Clara',
    'Roupa chinesa rosa com calca escura, dois coques no cabelo e bandana na testa.',
    'Roupa vermelha escura com detalhes orientais e bandana na testa.',
    62,
    'Especialista em armas ninja e combate a media distancia.',
    'Tenten e especialista em armas ninja e tecnicas de invocacao de armamentos. Durante a guerra, chegou a utilizar ferramentas lendarias do Sabio dos Seis Caminhos.',
    'Vivo'
);
''')

#TIME AREIA
cursor.execute('''
INSERT INTO Personagens (
    IdTipoPersonagem,
    IdCla,
    IdArcoAparicao,
    IdArcoMorte,
    IdOcupacaoClassico,
    IdOcupacaoShippuden,
    IdVila,
    Nome,
    Sobrenome,
    IdadeClasico,
    IdadeShippuden,
    Sexo,
    DataNascimento,
    AlturaClassico,
    AlturaShippuden,
    CorCabelo,
    CorOlhos,
    CorPele,
    DescricaoRoupaClassico,
    DescricaoRoupaShippuden,
    MissoesCompletas,
    Descricao,
    HistoriaPersonagem,
    Estado
)
VALUES

-- BAKI
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Terciario'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Areia'),
    'Baki',
    NULL,
    30,
    34,
    'Masculino',
    '1970-01-01',
    1.78,
    1.78,
    'Castanho',
    'Preto',
    'Clara',
    'Roupa tradicional da Areia com tecido cobrindo parte do rosto e bandana na testa.',
    'Visual semelhante ao classico, mantendo traje da Areia e bandana na testa.',
    694,
    'Jounin da Vila da Areia e lider do time de Gaara.',
    'Baki foi o lider do time da Areia durante o Exame Chunin e participou da conspiracao com Orochimaru contra Konoha. Posteriormente ajudou na alianca entre as vilas.',
    'Vivo'
),

-- =========================
-- GAARA
-- =========================
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Principais'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Kazekage'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Areia'),
    'Gaara',
    NULL,
    12,
    16,
    'Masculino',
    '1987-01-19',
    1.48,
    1.68,
    'Vermelho',
    'Verde Claro',
    'Clara',
    'Roupa escura, faixa marrom segurando o cantil de areia nas costas e bandana na roupa, amor escrito na testa.',
    'Roupa longa vermelha do Kazekage, faixa branca na cintura e amor escrito na testa.',
    34,
    'Jinchuuriki do Shukaku e Quinto Kazekage.',
    'Gaara foi criado como arma da Vila da Areia por ser jinchuuriki do Shukaku. Inicialmente frio e violento, mudou apos lutar contra Naruto. Tornou-se o Quinto Kazekage e liderou sua vila durante a guerra.',
    'Vivo'
),

-- KANKURO
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Areia'),
    'Kankuro',
    NULL,
    14,
    18,
    'Masculino',
    '1986-05-15',
    1.65,
    1.75,
    'Castanho',
    'Preto',
    'Clara',
    'Roupa preta com capuz, pintura facial roxa e bandana na testa.',
    'Roupa preta com pintura facial mais detalhada e bandana na testa.',
    43,
    'Especialista em marionetes da Vila da Areia.',
    'Kankuro e especialista em combate com marionetes. Lutou contra Sasori e posteriormente tornou-se comandante de divisao durante a guerra.',
    'Vivo'
),

-- =========================
-- TEMARI
-- =========================
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Secundarios'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Genin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Jounin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Areia'),
    'Temari',
    NULL,
    15,
    19,
    'Feminino',
    '1985-08-23',
    1.57,
    1.65,
    'Loiro',
    'Verde',
    'Clara',
    'Roupa roxa clara com grande leque nas costas e bandana no pescoco.',
    'Roupa clara com faixa vermelha na cintura, grande leque de combate e bandana na testa.',
    42,
    'Especialista em tecnicas de vento da Vila da Areia.',
    'Temari e usuaria de tecnicas de vento utilizando um grande leque. Demonstrou grande habilidade estrategica e participou da alianca shinobi na guerra.',
    'Vivo'
);
''')

#VILOES
cursor.execute('''
INSERT INTO Ocupacoes (Nome) VALUES
    ('Nukenin'),
    ('Senhor Feudal'),
    ('Criminoso'),
    ('Servo de Orochimaru');
''')

cursor.execute('''
INSERT INTO Clas (Nome, Descricao) VALUES
('Kaguya', 'Cla de natureza guerreira e Kekkei Genkai Shikotsumyaku, que permite manipular e transformar os próprios ossos em armas letais.');
''')

cursor.execute('''
    INSERT INTO Personagens (
    IdTipoPersonagem,
    IdCla,
    IdArcoAparicao,
    IdArcoMorte,
    IdOcupacaoClassico,
    IdOcupacaoShippuden,
    IdVila,
    Nome,
    Sobrenome,
    IdadeClasico,
    IdadeShippuden,
    Sexo,
    DataNascimento,
    AlturaClassico,
    AlturaShippuden,
    CorCabelo,
    CorOlhos,
    CorPele,
    DescricaoRoupaClassico,
    DescricaoRoupaShippuden,
    MissoesCompletas,
    Descricao,
    HistoriaPersonagem,
    Estado
)
VALUES
               
-- OROCHIMARU
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Orochimaru',
    NULL,
    50,
    54,
    'Masculino',
    '1950-10-27',
    1.79,
    1.79,
    'Preto',
    'Amarelo',
    'Clara',
    'Roupas claras com corda roxa grossa na cintura, cabelos longos, lingua de serpente',
    'Visual semelhante ao classico, mantendo corda roxa e aparencia serpentina.',
    1468,
    'Um dos Sannin Lendarios e antigo ninja da Folha.',
    'Orochimaru foi aluno do Terceiro Hokage e tornou-se um dos Sannin Lendarios. Abandonou Konoha apos realizar experimentos proibidos e fundou a Vila do Som. Buscou a imortalidade e o corpo perfeito.',
    'Vivo'
),

-- KABUTO YAKUSHI

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Exame Chunin'),
    NULL,
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Kabuto',
    'Yakushi',
    19,
    23,
    'Masculino',
    '1980-02-29',
    1.77,
    1.77,
    'Cinza',
    'Preto',
    'Clara',
    'Uniforme ninja padrao com oculos redondos e bandana da Folha.',
    'Visual modificado com caracteristicas serpentescas apos absorver DNA de Orochimaru.',
    191,
    'Espiao e assistente de Orochimaru.',
    'Kabuto foi criado como espiao e tornou-se seguidor fiel de Orochimaru. Durante a guerra, dominou o Edo Tensei e transformou-se fisicamente ao modificar seu proprio corpo.',
    'Vivo'
),

-- =========================
-- ZABUZA MOMOCHI
-- =========================
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Pais das Ondas'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Pais das Ondas'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Nevoa'),
    'Zabuza',
    'Momochi',
    26,
    NULL,
    'Masculino',
    '1970-08-15',
    1.83,
    NULL,
    'Preto',
    'Preto',
    'Clara',
    'Roupa escura com ataduras cobrindo a boca, espada Kubikiribocho nas costas e bandana riscada da Nevoa.',
    NULL,
    191,
    'Ex-membro dos Sete Espadachins da Nevoa.',
    'Zabuza era conhecido como o Demonio da Nevoa. Tornou-se nukenin apos tentativa de golpe na vila. Trabalhou como mercenario e enfrentou o Time 7 na Missao no Pais das Ondas.',
    'Morto'
),

-- HAKU
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Pais das Ondas'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Pais das Ondas'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Criminoso'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Nevoa'),
    'Haku',
    NULL,
    15,
    NULL,
    'Masculino',
    '1981-01-09',
    1.55,
    NULL,
    'Preto',
    'Castanho',
    'Clara',
    'Kimono claro com mascara de caçador da Nevoa',
    NULL,
    NULL,
    'Usuario da Kekkei Genkai de Gelo.',
    'Haku possuia a Kekkei Genkai de gelo e foi perseguido por isso. Foi acolhido por Zabuza e tornou-se seu aliado fiel. Morreu protegendo Zabuza durante a batalha na ponte.',
    'Morto'
),
               
-- ITACHI UCHIHA

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Uchiha'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Ataque a Vila da Folha'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Batalha Fadidica entre Irmaos'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Folha'),
    'Itachi',
    'Uchiha',
    17,
    21,
    'Masculino',
    '1986-06-09',
    1.75,
    1.78,
    'Preto',
    'Preto',
    'Clara',
    'Manto preto da Akatsuki com nuvens vermelhas e bandana riscada da Folha.',
    'Manto preto da Akatsuki com nuvens vermelhas e bandana riscada da Folha.',
    340,
    'Membro da Akatsuki e prodigio do cla Uchiha.',
    'Itachi exterminou seu proprio cla sob ordens secretas para evitar uma guerra civil. Viveu como vilao aos olhos do mundo para proteger Konoha e seu irmao Sasuke.',
    'Morto'
),

-- KISAME HOSHIGAKI
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Hoshigake'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Ataque a Vila da Folha'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Quarta Grande Guerra Ninja: Confronto'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Nukenin'),
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila Oculta da Nevoa'),
    'Kisame',
    'Hoshigaki',
    29,
    33,
    'Masculino',
    '1974-03-18',
    1.95,
    1.95,
    'Azul Escuro',
    'Pequenos e Brancos',
    'Azulada',
    'Manto da Akatsuki com nuvens vermelhas e bandana riscada da Nevoa.',
    'Manto da Akatsuki com nuvens vermelhas e bandana riscada da Nevoa.',
    332,
    'Membro da Akatsuki conhecido como o Monstro da Nevoa.',
    'Kisame foi membro dos Sete Espadachins da Nevoa e parceiro de Itachi na Akatsuki. Suicidou-se para proteger informacoes da organizacao.',
    'Morto'
),

-- KIMIMARO
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    (SELECT IdCla FROM Clas WHERE Nome = 'Kaguya'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Servo de Orochimaru'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila do Som'),
    'Kimimaro',
    NULL,
    15,
    NULL,
    'Masculino',
    '1988-06-15',
    1.66,
    NULL,
    'Branco',
    'Verde',
    'Clara',
    'Roupa cinza clara com faixa roxa',
    NULL,
    22,
    'Ultimo sobrevivente do cla Kaguya.',
    'Kimimaro possuia a Kekkei Genkai Shikotsumyaku, capaz de manipular seus ossos. Extremamente leal a Orochimaru, morreu devido a uma doenca rara.',
    'Morto'
),

-- TAYUYA

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Servo de Orochimaru'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila do Som'),
    'Tayuya',
    NULL,
    14,
    NULL,
    'Feminino',
    '1989-02-15',
    1.48,
    NULL,
    'Vermelho',
    'Preto',
    'Clara',
    'Roupa bege com faixa roxa e bandana riscada.',
    NULL,
    46,
    'Especialista em genjutsu sonoro do Quarteto do Som.',
    'Tayuya utilizava uma flauta para controlar invocacoes demonicas e aplicar genjutsu. Foi derrotada por Shikamaru e Temari.',
    'Morto'
),

-- SAKON E UKON

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Servo de Orochimaru'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila do Som'),
    'Sakon/Ukon',
    NULL,
    14,
    NULL,
    'Masculino',
    '1989-05-20',
    1.55,
    NULL,
    'Cinza',
    'Azul',
    'Clara',
    'Roupa bege com faixa roxa.',
    NULL,
    46,
    'Irmãos capazes de fundir seus corpos.',
    'Sakon e Ukon compartilhavam um corpo duplo e podiam fundir-se ao inimigo. Foram derrotados por Kiba e Kankuro.',
    'Morto'
),

-- JIROBO

(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Servo de Orochimaru'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila do Som'),
    'Jirobo',
    NULL,
    14,
    NULL,
    'Masculino',
    '1989-04-10',
    1.81,
    NULL,
    'Laranja',
    'Preto',
    'Clara',
    'Roupa bege com faixa roxa',
    NULL,
    46,
    'Membro mais forte fisicamente do Quarteto do Som.',
    'Jirobo utilizava tecnicas de terra e absorcao de chakra. Foi derrotado por Choji Akimichi.',
    'Morto'
),

-- KIDOMARO
               
(
    (SELECT IdTipoPersonagem FROM TipoPersonagens WHERE Relevancia = 'Antagonista'),
    NULL,
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdArco FROM Arcos WHERE Nome = 'Missao de Recuperacao de Sasuke'),
    (SELECT IdOcupacao FROM Ocupacoes WHERE Nome = 'Servo de Orochimaru'),
    NULL,
    (SELECT IdVila FROM Vilas WHERE Nome = 'Vila do Som'),
    'Kidomaru',
    NULL,
    14,
    NULL,
    'Masculino',
    '1989-12-16',
    1.59,
    NULL,
    'Castanho Escuro',
    'Preto',
    'Clara',
    'Roupa bege com faixa roxa na cintura, seis bracos adicionais em combate.',
    NULL,
    46,
    'Especialista em ataques de longa distancia do Quarteto do Som.',
    'Kidomaru possui habilidades semelhantes a uma aranha, podendo produzir teias extremamente resistentes e formar armaduras e armas com seu chakra. Lutou contra Neji Hyuga e foi derrotado apos combate estrategico intenso.',
    'Morto'
);
''')

conn.commit()

print("INSERT REALIZADO")
