from DataBase.databaseConfig import cursor, conn

cursor.execute("""
TRUNCATE TABLE 
PersonagensAtributosDatabook,
PersonagensHabilidades,
Habilidades,
Databooks,
PersonagensElementos,
PersonagensJutsus,
Jutsus,
Personagens,
Elementos,
TiposElementos,
TiposJutsu,
Ocupacoes,
Vilas,
Arcos,
Clas,
TipoPersonagens
RESTART IDENTITY CASCADE;
""")

cursor.execute("""
INSERT INTO TipoPersonagens (Relevancia) VALUES
('Protagonista'),
('Deuteragonista'),
('Antagonista'),
('Principais'),
('Secundarios'),
('Terciario');
""")

cursor.execute("""
INSERT INTO Clas (Nome, Descricao) VALUES
('Uzumaki', 'Clã conhecido por sua enorme vitalidade, grande reserva de chakra e domínio avançado de técnicas de selamento.'),
('Hatake', 'Clã respeitado de Konoha, famoso por ninjas como Kakashi e Sakumo'),
('Uchiha', 'Clã poderoso descendente de Indra, portador do Sharingan e conhecido por seu talento excepcional em combate.'),
('Haruno', 'Clã de origem civil em Konoha.'),
('Senju', 'Clã lendário rival dos Uchiha, conhecido por sua vitalidade e liderança.'),
('Hyuga', 'Clã portador do Byakugan, especializado em combate corpo a corpo e controle de chakra.'),
('Sarutobi', 'Clã tradicional de Konoha, conhecido por sua versatilidade e lealdade.'),
('Nara', 'Clã estrategista especializado em técnicas de manipulação de sombras.'),
('Akimichi', 'Clã que utiliza técnicas de expansão corporal baseadas em calorias.'),
('Yamanaka', 'Clã especializado em técnicas mentais e transferência de consciência.'),
('Aburame', 'Clã que utiliza insetos como arma em combate.'),
('Inuzuka', 'Clã que luta em parceria com cães ninjas.'),
('Namikaze', 'Clã pouco conhecido da vila da folha'),
('Hoshigake', 'Clã da Névoa associado a membros com caracteristicas animais');
""")

cursor.execute("""
INSERT INTO Arcos (Nome, Descricao) VALUES
('Prologo', 'Introdução da história de Naruto, apresentando o Time 7 e a vida inicial na Vila da Folha.'),
('Pais das Ondas', 'Primeira missão real do Time 7, enfrentando Zabuza e Haku em defesa de Tazuna.'),
('Exame Chunin', 'Competição entre vilas para promoção de ninjas, marcada por lutas intensas e invasão surpresa.'),
('Ataque a Vila da Folha', 'Invasão liderada por Orochimaru durante o Exame Chunin, resultando na morte do Terceiro Hokage.'),
('Busca por Tsunade', 'Naruto e Jiraiya procuram Tsunade para assumir o posto de Quinta Hokage.'),
('Missao de Recuperacao de Sasuke', 'Equipe formada para impedir que Sasuke abandone Konoha e se una a Orochimaru.'),
('Missao de Resgate do Kazekage', 'Akatsuki sequestra Gaara e o Time 7 parte para resgata-lo.'),
('Missao de Reconhecimento na Ponte Tenchi', 'Time Kakashi enfrenta Orochimaru e reencontra Sasuke.'),
('Missao de Supressao da Akatsuki', 'Shikamaru lidera equipe contra Hidan e Kakuzu.'),
('Missao de Busca por Itachi', 'Equipe formada para localizar Itachi Uchiha.'),
('Missao de Captura de Tres Caudas', 'Akatsuki tenta capturar o Sanbi.'),
('Perseguicao de Itachi', 'Sasuke rastreia Itachi para confronto final.'),
('Historia de Jiraiya, o Destemido', 'Jiraiya invade a vila da chuva para investigar Pain.'),
('Batalha Fadidica entre Irmaos', 'Confronto final entre Sasuke e Itachi.'),
('Invasao de Pain', 'Pain ataca Konoha em busca de Naruto.'),
('Cupula dos Cinco Kage', 'Reuniao das cinco grandes vilas ninja.'),
('Quarta Grande Guerra Ninja: Preparativos', 'Alianca Shinobi se organiza para guerra.'),
('Quarta Grande Guerra Ninja: Confronto', 'Grandes batalhas contra exercito de Zetsu e Edo Tensei'),
('Quarta Grande Guerra Ninja: Climax', 'Madara e Obito revelam plano final.'),
('Kaguya Otsutsuki e o Fim da Guerra', 'Naruto e Sasuke enfrentam Kaguya e encerram o conflito.');
""")

cursor.execute("""
INSERT INTO Vilas (Nome, Pais) VALUES
('Vila Oculta da Folha', 'Fogo'),
('Vila Oculta da Areia', 'Vento'),
('Vila Oculta da Nevoa', 'Agua'),
('Vila Oculta da Nuvem', 'Relampago'),
('Vila Oculta da Pedra', 'Terra'),
('Vila do Ferro', 'Ferro'),
('Vila do Som', 'Som'),
('Vila da Chuva', 'Chuva'),
('Vila da Grama', 'Grama');
""")

cursor.execute("""
INSERT INTO Ocupacoes (Nome) VALUES
('Genin'),
('Chunin'),
('Jounin'),
('Jounin especial'),
('Hokage'),
('Kazekage'),
('Mizukage'),
('Raikage'),
('Tsuchikage'),
('Civil'),
('Invocacao');
""")

cursor.execute("""
INSERT INTO TiposElementos (Nome) VALUES
('Elemento Basico'),
('Kekkei Genkai'),
('Kekkei Touta');
""")

cursor.execute("""
INSERT INTO TiposJutsu (Nome) VALUES
('Taijutsu'),
('Genjutsu'),
('Ninjutsu'),
('Fuuinjutsu'),
('Ninjutsu Medico'),
('Kinjutsu'),
('Nenhum');
""")

cursor.execute("""
INSERT INTO Elementos (IdTiposElementos, Nome) VALUES
(1,'Fogo'),
(1,'Agua'),
(1,'Terra'),
(1,'Relampago'),
(1,'Vento'),
(1,'Yin-Yang'),
(2,'Gelo'),
(2,'Lava'),
(2,'Vapor'),
(2,'Explosao'),
(3,'Poeira'),
(1,'Nenhum');
""")

# =========================
# PERSONAGENS
# =========================

cursor.execute("""
INSERT INTO Personagens (
    IdTipoPersonagem, IdCla, IdArcoAparicao,
    IdOcupacaoClassico, IdOcupacaoShippuden,
    IdVila,
    Nome, Sobrenome,
    IdadeClasico, IdadeShippuden,
    Sexo, DataNascimento,
    AlturaClassico, AlturaShippuden,
    CorCabelo, CorOlhos, CorPele,
    MissoesCompletas,
    Descricao,
    Estado
) VALUES

(1,1,1,1,1,1,
'Naruto','Uzumaki',
12,15,
'Masculino','1987-10-10',
145.00,166.00,
'Loiro','Azul','Clara',
7,
'Ninja que deseja se tornar Hokage.',
'Vivo'),

(2,3,1,1,1,1,
'Sasuke','Uchiha',
12,15,
'Masculino','1988-07-23',
150.00,168.00,
'Preto','Preto','Clara',
7,
'Prodigio do cla Uchiha.',
'Vivo'),

(4,4,1,1,1,1,
'Sakura','Haruno',
12,15,
'Feminino','1988-03-28',
148.00,161.00,
'Rosa','Verde','Clara',
7,
'Ninja medica do Time 7.',
'Vivo'),

(4,2,1,3,3,1,
'Kakashi','Hatake',
26,29,
'Masculino','1961-09-15',
181.00,181.00,
'Prata','Cinza','Clara',
1000,
'Jounin lider do Time 7.',
'Vivo');
""")

# =========================
# JUTSUS
# =========================

cursor.execute("""
INSERT INTO Jutsus (IdElemento, IdTipoJutsu, Nome, Descricao, Rank) VALUES
(12,3,'Clone das Sombras','Cria copias fisicas.','B'),
(12,3,'Rasengan','Esfera concentrada de chakra.','A'),
(4,3,'Chidori','Ataque de relampago.','A'),
(1,3,'Bola de Fogo','Tecnica classica Uchiha.','C'),
(1,3,'Flor de Fenix','Multiplas bolas de fogo.','C'),
(12,2,'Sharingan','Doujutsu Uchiha.','A'),
(2,3,'Dragao de Agua','Dragao feito de agua.','B'),
(2,3,'Vortex de Agua','Turbilhao de agua.','B'),
(3,3,'Cacador de Cabecas','Tecnica de terra.','C');
""")

cursor.execute("""
INSERT INTO PersonagensJutsus VALUES
(1,1),(1,2),
(2,3),(2,4),(2,5),(2,6),
(4,3),(4,7),(4,8),(4,9);
""")

cursor.execute("""
INSERT INTO PersonagensElementos VALUES
(1,5),
(2,1),(2,4),
(4,1),(4,2),(4,3),(4,4),(4,5);
""")

# =========================
# HABILIDADES
# =========================

cursor.execute("""
INSERT INTO Habilidades (Nome, Descricao) VALUES
('Estrategista','Alta capacidade de analise em combate.'),
('Controle de Chakra','Controle refinado de chakra.'),
('Velocidade Elevada','Movimentos extremamente rapidos.'),
('Forca Elevada', 'Capaz de nocautear e destruir campos de batalha com forca bruta');
""")

cursor.execute("""
INSERT INTO PersonagensHabilidades VALUES
(1,2),
(2,3),
(4,1);
""")

# =========================
# DATABOOKS
# =========================

cursor.execute("""
INSERT INTO Databooks (Edicao, Descricao) VALUES
(1,'Databook Classico 1'),
(2,'Databook Final Classico'),
(3,'Databook Shippuden'),
(4,'Databook Meio Shippuden');
""")

# =========================
# ATRIBUTOS DATABOOK
# =========================

cursor.execute("""
INSERT INTO PersonagensAtributosDatabook VALUES
(1,1,3.5,3.0,1.0,2.5,3.0,3.5,4.0,2.0),
(2,1,3.0,3.5,2.0,3.0,3.0,4.0,3.0,3.5),
(4,1,4.5,4.5,3.5,5.0,4.0,4.5,4.5,5.0);
""")

conn.commit()

print("SEED COMPLETA EXECUTADA COM SUCESSO!")
