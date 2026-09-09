import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'instance/flaskr.sqlite' # Ajuste o caminho se o seu banco estiver em outro diretório (ex: instance/banco.sqlite)

def seed_database():
    print("Conectando ao banco de dados...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Habilita suporte a chaves estrangeiras no SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Cria um usuário de teste (Admin) se não existir
    cursor.execute("SELECT id FROM user WHERE username = 'admin_teste';")
    user = cursor.fetchone()
    
    if not user:
        hashed_password = generate_password_hash('123456')
        cursor.execute(
            "INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?);",
            ('admin_teste', hashed_password, 1)
        )
        user_id = cursor.lastrowid
        print(f"-> Usuário de teste criado com ID: {user_id}")
    else:
        user_id = user[0]
        print(f"-> Usando usuário existente com ID: {user_id}")

    # 2. Criação da Prova 1: 10 Questões, 4 Alternativas cada
    cursor.execute(
        "INSERT INTO provas (author_id_fk, titulo, serie, materia) VALUES (?, ?, ?, ?);",
        (user_id, 'Simulado de Matemática Básica', '3º Ano EM', 'Matemática')
    )
    prova1_id = cursor.lastrowid
    print(f"-> Prova 1 criada (ID: {prova1_id}) - 10 questões / 4 alternativas")

    for i in range(1, 11):
        enunciado = f"Qual é o resultado da operação matemática da questão número {i}?"
        # Definimos a alternativa C (índice 2) como a correta para simplificar o seed
        correta_index = 2 
        
        alternativas_p1 = [
            f"Resposta incorreta A para a questão {i}",
            f"Resposta incorreta B para a questão {i}",
            f"Resposta CORRETA C para a questão {i}",
            f"Resposta incorreta D para a questão {i}"
        ]
        
        gabarito_texto = alternativas_p1[correta_index]

        # Insere a questão
        cursor.execute(
            "INSERT INTO questoes (prova_id_fk, enunciado, resposta) VALUES (?, ?, ?);",
            (prova1_id, enunciado, gabarito_texto)
        )
        questao_id = cursor.lastrowid

        # Insere as 4 alternativas
        for idx, alt_texto in enumerate(alternativas_p1):
            is_correct = 1 if idx == correta_index else 0
            cursor.execute(
                "INSERT INTO questoes_alternativas (questao_id_fk, alternativa, is_correct) VALUES (?, ?, ?);",
                (questao_id, alt_texto, is_correct)
            )

    # 3. Criação da Prova 2: 5 Questões, 5 Alternativas cada
    cursor.execute(
        "INSERT INTO provas (author_id_fk, titulo, serie, materia) VALUES (?, ?, ?, ?);",
        (user_id, 'Simulado de História Geral', '2º Ano EM', 'História')
    )
    prova2_id = cursor.lastrowid
    print(f"-> Prova 2 criada (ID: {prova2_id}) - 5 questões / 5 alternativas")

    for j in range(1, 6):
        enunciado = f"Sobre os eventos históricos abordados no tópico {j}, assinale a alternativa correta:"
        # Definimos a alternativa E (índice 4) como a correta nesta prova
        correta_index_p2 = 4

        alternativas_p2 = [
            f"Fato histórico incorreto A da questão {j}",
            f"Fato histórico incorreto B da questão {j}",
            f"Fato histórico incorreto C da questão {j}",
            f"Fato histórico incorreto D da questão {j}",
            f"Fato histórico CORRETO E da questão {j}"
        ]

        gabarito_texto_p2 = alternativas_p2[correta_index_p2]

        # Insere a questão
        cursor.execute(
            "INSERT INTO questoes (prova_id_fk, enunciado, resposta) VALUES (?, ?, ?);",
            (prova2_id, enunciado, gabarito_texto_p2)
        )
        questao_id = cursor.lastrowid

        # Insere as 5 alternativas
        for idx, alt_texto in enumerate(alternativas_p2):
            is_correct = 1 if idx == correta_index_p2 else 0
            cursor.execute(
                "INSERT INTO questoes_alternativas (questao_id_fk, alternativa, is_correct) VALUES (?, ?, ?);",
                (questao_id, alt_texto, is_correct)
            )

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()
    print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    seed_database()