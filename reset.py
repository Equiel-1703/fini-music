

def __drop_schema(cur):
    cur.execute("DROP SCHEMA IF EXISTS public CASCADE")


def __create_tables(cur):
    cur.execute("CREATE SCHEMA public")

    cur.execute("CREATE TABLE usuario ("
                "email_usuario VARCHAR(50) PRIMARY KEY,"
                "nome_usuario VARCHAR(50) NOT NULL,"
                "senha VARCHAR(50) NOT NULL,"
                "foto_perfil bytea )")
    print("Table usuario created successfully in PostgreSQL")

    cur.execute("CREATE TABLE playlist ( "
                "id_playlist SERIAL,"
                "nome_playlist varchar(100) not null,"
                "email_usuario varchar(250) not null,"
                "PRIMARY KEY (id_playlist),"
                "FOREIGN KEY (email_usuario) REFERENCES usuario(email_usuario) )")
    print("Table playlist created successfully in PostgreSQL")

    cur.execute("CREATE TABLE artista ("
                "id_artista SERIAL,"
                "nome_artista varchar(100) not null,"
                "descricao text not null,"
                "foto bytea,"
                "PRIMARY KEY (id_artista) )")
    print("Table artista created successfully in PostgreSQL")

    cur.execute("CREATE TABLE album ( "
                "id_album SERIAL,"
                "nome_album varchar(100) not null,"
                "capa bytea,"
                "id_artista integer not null,"
                "PRIMARY KEY (id_album),"
                "FOREIGN KEY (id_artista) REFERENCES artista(id_artista) )")
    print("Table album created successfully in PostgreSQL")

    cur.execute("CREATE TABLE musica ("
                "id_musica SERIAL,"
                "nome_musica varchar(100) not null,"
                "visualizacoes integer default 0 not null,"
                "id_album integer,"
                "duracao integer not null,"
                "file bytea,"
                "PRIMARY KEY (id_musica),"
                "FOREIGN KEY (id_album) REFERENCES album(id_album) )")
    print("Table musica created successfully in PostgreSQL")

    cur.execute("CREATE TABLE genero ("
                "id_genero SERIAL,"
                "nome_genero varchar(60),"
                "PRIMARY KEY (id_genero) )")
    print("Table genero created successfully in PostgreSQL")

    cur.execute("CREATE TABLE genero_musica ("
                "id_genero integer not null,"
                "id_musica integer not null,"
                "PRIMARY KEY (id_genero, id_musica),"
                "FOREIGN KEY (id_genero) REFERENCES genero(id_genero),"
                "FOREIGN KEY (id_musica) REFERENCES musica(id_musica) )")
    print("Table genero_musica created successfully in PostgreSQL")

    cur.execute("CREATE TABLE playlist_musica ("
                "id_musica integer,"
                "id_playlist integer,"
                "PRIMARY KEY (id_musica, id_playlist),"
                "FOREIGN KEY (id_playlist) REFERENCES playlist(id_playlist),"
                "FOREIGN KEY (id_musica) REFERENCES musica(id_musica) )")
    print("Table playlist_musica created successfully in PostgreSQL")


def __get_mp3_binary_for_sql(mp3_file_path):
    return f"'\\x{open(mp3_file_path, 'rb').read().hex()}'::bytea"


def __insert_values(cur):
    cur.execute("INSERT INTO artista (nome_artista, descricao) VALUES"
                "('System of a Down', 'System of a Down eh uma banda de metal.'),"
                "('Linkin Park', 'Linkin Park eh uma banda de rock.'),"
                "('Nirvana', 'Nirvana foi uma banda.'),"
                "('Eminem', 'Eminem eh o autor do hit assaromalonaminanevagettinnthifmetrkls.'),"
                "('Olivia Rodrigo', 'OMG its olivia rodrigo!')")

    cur.execute("INSERT INTO album (nome_album, capa, id_artista) VALUES"
                "('Toxicity', null, 1),"
                "('Hypnotize', null, 1),"
                "('Hybrid Theory', null, 2),"
                "('Meteora', null, 2),"
                "('Nevermind', null, 3),"
                "('In Utero', null, 3),"
                "('The Real Slim Shady LP', null, 4),"
                "('Sour', null, 5)")

    cur.execute("INSERT INTO musica (nome_musica, duracao, id_album, file) VALUES"
                f"('Chop Suey', 209, 1, {__get_mp3_binary_for_sql('musics/chop_suey.mp3')}),"
                f"('Aerials', 244, 1, {__get_mp3_binary_for_sql('musics/aerials.mp3')}),"
                f"('Lost in Hollywood', 323, 2, {__get_mp3_binary_for_sql('musics/lost_in_hollywood.mp3')}),"
                f"('In The End', 218, 3, {__get_mp3_binary_for_sql('musics/in_the_end.mp3')}),"
                f"('Numb', 187, 4, {__get_mp3_binary_for_sql('musics/numb.mp3')}),"
                f"('Crawling', 216, 3, {__get_mp3_binary_for_sql('musics/crawling.mp3')}),"
                f"('Smells Like Teen Spirit', 278, 5, {__get_mp3_binary_for_sql('musics/smells_like_teen_spirit.mp3')}),"
                f"('Heart-Shaped Box', 282, 6, {__get_mp3_binary_for_sql('musics/heart_shaped_box.mp3')}),"
                f"('Come As You Are', 224, 5, {__get_mp3_binary_for_sql('musics/come_as_you_are.mp3')}),"
                f"('My Name Is', 268, 7, {__get_mp3_binary_for_sql('musics/my_name_is.mp3')}),"
                f"('good 4 u', 178, 8, {__get_mp3_binary_for_sql('musics/good_4_u.mp3')}),"
                f"('brutal', 143, 8, {__get_mp3_binary_for_sql('musics/brutal.mp3')})")

    cur.execute("INSERT INTO genero (nome_genero) VALUES"
                "('Rock'),"  # 1
                "('Metal'),"  # 2
                "('Rap'),"  # 3
                "('Hip-Hop'),"  # 4
                "('Pop'),"  # 5
                "('Indie'),"  # 6
                "('Grunge')")  # 7

    cur.execute("INSERT INTO genero_musica (id_genero,id_musica) VALUES"
                "(1, 1),"
                "(2, 1),"
                "(1, 2),"
                "(2, 2),"
                "(1, 3),"
                "(2, 3),"
                "(1, 4),"
                "(6, 4),"
                "(1, 5),"
                "(6, 5),"
                "(1, 6),"
                "(6, 6),"
                "(1, 7),"
                "(7, 7),"
                "(1, 8),"
                "(7, 8),"
                "(1, 9),"
                "(7, 9),"
                "(3, 10),"
                "(4, 10),"
                "(5, 11),"
                "(5, 12)")


def run(cur, conn):
    __drop_schema(cur)
    print("Old schema deleted successfully in PostgreSQL ")
    __create_tables(cur)
    print("Tables created successfully in PostgreSQL ")
    __insert_values(cur)
    print("Default values inserted successfully in PostgreSQL ")
    conn.commit()
