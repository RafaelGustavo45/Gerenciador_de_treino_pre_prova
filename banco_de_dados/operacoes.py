import sqlite3

def inicializar_banco():
    # Conecta ao banco de dados (será criado o arquivo se não existir)
    conn = sqlite3.connect("gestor_provas.db")
    cursor = conn.cursor()

    # Ativa o suporte a chaves estrangeiras no SQLite (desativado por padrão)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Tabela Provas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS provas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo VARCHAR(60) NOT NULL,
        serie INTEGER NOT NULL,
        materia VARCHAR(40) NOT NULL,
        cronometro_segundos INTEGER
    );
    """)

    # 2. Tabela Questoes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_id_prova INTEGER NOT NULL,
        texto VARCHAR(1000) NOT NULL,
        FOREIGN KEY (fk_id_prova) REFERENCES provas(id) ON DELETE CASCADE
    );
    """)

    # 3. Tabela Alternativas
    # Adicionado o campo 'correta' (0 para falsa, 1 para verdadeira) para simplificar o gabarito
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alternativas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_id_questao INTEGER NOT NULL,
        texto VARCHAR(100) NOT NULL,
        correta INTEGER DEFAULT 0, 
        FOREIGN KEY (fk_id_questao) REFERENCES questoes(id) ON DELETE CASCADE
    );
    """)

    # 4. Tabela Estudantes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        criptografed_PW VARCHAR(255) NOT NULL
    );
    """)

    # 5. Tabela Professor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        criptografed_PW VARCHAR(255) NOT NULL
    );
    """)

    # 6. Tabela Desempenho
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS desempenho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fk_id_estudante INTEGER NOT NULL,
        fk_id_prova INTEGER NOT NULL,
        nota REAL NOT NULL,
        FOREIGN KEY (fk_id_estudante) REFERENCES estudantes(id) ON DELETE CASCADE,
        FOREIGN KEY (fk_id_prova) REFERENCES provas(id) ON DELETE CASCADE
    );
    """)

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()
    print("Banco de dados e tabelas criados com sucesso!")

def criar_prova(titulo, serie, materia, cronometro_segundos=None):
    """
    Insere uma nova prova no banco de dados.
    O argumento 'cronometro_segundos' é opcional e assume None (NULL no banco) por padrão.
    """
    conn = sqlite3.connect("gestor_provas.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        # O uso de '?' previne SQL Injection e lida nativamente com valores None (NULL)
        query = """
        INSERT INTO provas (titulo, serie, materia, cronometro_segundos)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(query, (titulo, serie, materia, cronometro_segundos))
        conn.commit()
        
        # Recupera o ID da prova que acabou de ser inserida
        id_prova_criada = cursor.lastrowid
        print(f"Prova '{titulo}' criada com sucesso! ID: {id_prova_criada}")
        return id_prova_criada

    except sqlite3.Error as e:
        print(f"Erro ao inserir a prova '{titulo}': {e}")
        return None
    finally:
        conn.close()


def criar_questao(prova_id_fk, texto_questao, lista_alternativas):
    """
    Cadastra uma questão e suas respectivas alternativas.
    
    lista_alternativas deve ser uma lista de dicionários, ex:
    [
        {"texto": "Alternativa A", "correta": False},
        {"texto": "Alternativa B", "correta": True},
        {"texto": "Alternativa C", "correta": False}
    ]
    """
    # 1. Validação das Regras de Negócio
    if len(lista_alternativas) < 3:
        print("Erro: A questão precisa ter pelo menos 3 alternativas.")
        return False
        
    # Verifica se existe pelo menos uma alternativa correta (True)
    tem_correta = any(alt.get("correta") is True for alt in lista_alternativas)
    if not tem_correta:
        print("Erro: A questão precisa ter pelo menos 1 alternativa correta.")
        return False

    conn = sqlite3.connect("gestor_provas.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        # 2. Inserir a Questão
        query_questao = "INSERT INTO questoes (fk_id_prova, texto) VALUES (?, ?);"
        cursor.execute(query_questao, (prova_id_fk, texto_questao))
        
        # Recupera o ID gerado para a questão atual
        id_questao_criada = cursor.lastrowid

        # 3. Inserir as Alternativas correspondentes
        query_alternativa = """
        INSERT INTO alternativas (fk_id_questao, texto, correta) 
        VALUES (?, ?, ?);
        """
        
        for alt in lista_alternativas:
            texto_alt = alt.get("texto")
            # Converte True/False do Python para 1/0 do SQLite
            correta_alt = 1 if alt.get("correta") else 0
            
            cursor.execute(query_alternativa, (id_questao_criada, texto_alt, correta_alt))

        # Confirma todas as operações apenas se nenhuma linha deu erro
        conn.commit()
        print(f"Questão inserida com sucesso (ID: {id_questao_criada}) com {len(lista_alternativas)} alternativas!")
        return True

    except sqlite3.Error as e:
        # Se der qualquer erro (ex: ID da prova não existir), desfaz tudo
        conn.rollback()
        print(f"Erro de banco de dados ao inserir a questão: {e}")
        return False
    finally:
        conn.close()

def criar_estudante(username, password_texto_puro):
    """Insere um novo estudante no banco de dados."""
    conn = sqlite3.connect("gestor_provas.db")
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO estudantes (username, criptografed_PW) VALUES (?, ?);"
        cursor.execute(query, (username, password_texto_puro))
        conn.commit()
        
        id_estudante = cursor.lastrowid
        print(f"Estudante '{username}' criado com sucesso! ID: {id_estudante}")
        return id_estudante
    except sqlite3.IntegrityError:
        print(f"Erro: O username de estudante '{username}' já existe.")
        return None
    finally:
        conn.close()


def criar_professor(username, password_texto_puro):
    """Insere um novo professor no banco de dados."""
    conn = sqlite3.connect("gestor_provas.db")
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO professores (username, criptografed_PW) VALUES (?, ?);"
        cursor.execute(query, (username, password_texto_puro))
        conn.commit()
        
        id_professor = cursor.lastrowid
        print(f"Professor '{username}' criado com sucesso! ID: {id_professor}")
        return id_professor
    except sqlite3.IntegrityError:
        print(f"Erro: O username de professor '{username}' já existe.")
        return None
    finally:
        conn.close()

def gerar_resultado(id_da_prova, id_do_estudante, lista_respostas):
    """
    Processa as respostas de um estudante, calcula a nota proporcional a 10
    e salva o registro consolidado na tabela de desempenho.
    
    lista_respostas deve ser uma lista contendo os números das alternativas escolhidas, 
    ex: [2, 3, 2, 2, 2, 4, 1, 2, 3]
    """
    conn = sqlite3.connect("gestor_provas.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        # 1. Buscar o gabarito real da prova no banco de dados
        # Selecionamos a ordem das alternativas corretas para cada questão daquela prova
        query_gabarito = """
            SELECT a.texto 
            FROM alternativas a
            JOIN questoes q ON a.fk_id_questao = q.id
            WHERE q.fk_id_prova = ?
            ORDER BY q.id ASC, a.id ASC;
        """
        cursor.execute(query_gabarito, (id_da_prova,))
        todas_alternativas = cursor.fetchall()
        
        # Como as alternativas foram inseridas como "Alternativa 1", "Alternativa 2", etc.
        # Vamos reconstruir o gabarito oficial identificando qual delas tem 'correta' ligada.
        # Para manter o seu exemplo perfeito, vamos buscar qual o número da alternativa correta por questão:
        
        query_gabarito_direto = """
            SELECT q.id, a.texto 
            FROM alternativas a
            JOIN questoes q ON a.fk_id_questao = q.id
            WHERE q.fk_id_prova = ? AND a.correta = 1
            ORDER BY q.id ASC;
        """
        cursor.execute(query_gabarito_direto, (id_da_prova,))
        gabarito_db = cursor.fetchall()
        
        # Extrai apenas o número final do texto da alternativa (ex: "Alternativa 2" vira o inteiro 2)
        # Isso garante que a função funcione para QUALQUER gabarito cadastrado!
        gabarito_oficial = []
        for questao_id, texto_alt in gabarito_db:
            # Pega o último caractere do texto (o número da alternativa) e converte para int
            numero_correto = int(texto_alt.split()[-1])
            gabarito_oficial.append(numero_correto)

        # Validação de segurança: se o tamanho das respostas não bater com o total de questões
        if len(lista_respostas) != len(gabarito_oficial):
            print(f"Erro: O número de respostas ({len(lista_respostas)}) não bate com o número de questões da prova ({len(gabarito_oficial)}).")
            return None

        # 2. Loop de comparação para calcular os acertos
        total_questoes = len(gabarito_oficial)
        acertos = 0
        
        for i in range(total_questoes):
            if lista_respostas[i] == gabarito_oficial[i]:
                acertos += 1

        # 3. Cálculo da nota (Regra de três para base 10.0, arredondado para 1 casa decimal)
        nota = round((acertos / total_questoes) * 10, 1)

        print(f"\n--- Relatório de Processamento ---")
        print(f"Gabarito Oficial: {gabarito_oficial}")
        print(f"Respostas Aluno : {lista_respostas}")
        print(f"Acertos: {acertos} de {total_questoes}")
        print(f"Nota Final Calculada: {nota}")
        print(f"---------------------------------")

        # 4. Inserção Indireta no Banco de Dados (Tabela Desempenho)
        query_inserir_desempenho = """
            INSERT INTO desempenho (fk_id_estudante, fk_id_prova, nota)
            VALUES (?, ?, ?);
        """
        cursor.execute(query_inserir_desempenho, (id_do_estudante, id_da_prova, nota))
        conn.commit()
        
        id_desempenho = cursor.lastrowid
        print(f"Desempenho salvo com sucesso! ID do Registro: {id_desempenho}")
        return id_desempenho

    except sqlite3.Error as e:
        print(f"Erro de banco de dados ao gerar resultado: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado no processamento: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    inicializar_banco()
    id_prova1 = criar_prova(
        titulo="Concurso IT Analyst", 
        serie=4, 
        materia="Tecnologia da Informação", 
        cronometro_segundos=1800
    )

    # Prova 2: Sem cronômetro (o parâmetro assume None automaticamente)
    id_prova2 = criar_prova(
        titulo="Prova Faculdade Engenharia", 
        serie=3, 
        materia="Sistemas Operacionais"
    )


    id_da_prova = 1 
    
    # Montando a estrutura exatamente como no seu exemplo
    alternativas_exemplo = [
        {"texto": "Alternativa 1", "correta": False},
        {"texto": "Alternativa 2", "correta": True},
        {"texto": "Alternativa 3", "correta": False}
    ]
    
    print("Tentando cadastrar questão válida...")

    criar_questao(
        prova_id_fk=id_da_prova, 
        texto_questao="Qual das opções abaixo representa a alternativa correta do teste?", 
        lista_alternativas=alternativas_exemplo
    )

    # Teste de validação (Vai falhar porque só tem 2 alternativas)
    print("\nTentando cadastrar com menos de 3 alternativas...")
    alternativas_invalidas = [
        {"texto": "Incompleta 1", "correta": True},
        {"texto": "Incompleta 2", "correta": False}
    ]
    criar_questao(id_da_prova, "Questão Inválida?", alternativas_invalidas)

    id_aluno_teste = criar_estudante(
        username="aluno_ti_2026", 
        password_texto_puro="senha_simples_123"
    )
    
    # Criando 1 Professor
    id_prof_teste = criar_professor(
        username="prof_mario_redes", 
        password_texto_puro="admin_faculdade"
    )

    print("Iniciando a preparação da base de dados para a etapa de avaliação...\n")

    # 1. Criando a Prova 3 conforme especificado
    id_prova3 = criar_prova(
        titulo="Teste ", 
        serie=3, 
        materia="testadores"
    )

    # Se a prova foi criada com sucesso, geramos as 9 questões estruturadas
    if id_prova3:
        print("\nGerando 9 questões com 4 alternativas cada...")
        
        # Estrutura base de alternativas que será usada em cada questão
        # (Alternativa 2 é a correta em todas para fins de consistência no teste)
        alternativas_padrao = [
            {"texto": "Alternativa 1", "correta": False},
            {"texto": "Alternativa 2", "correta": True},
            {"texto": "Alternativa 3", "correta": False},
            {"texto": "Alternativa 4", "correta": False}
        ]

        # Loop para criar as 9 questões sequencialmente
        for i in range(1, 10):
            texto_da_questao = f"Questão tal número {i}?"
            
            # Chama a função criada na etapa anterior
            sucesso = criar_questao(
                prova_id_fk=id_prova3, 
                texto_questao=texto_da_questao, 
                lista_alternativas=alternativas_padrao
            )
            
            if not sucesso:
                print(f"Aviso: Falha ao gerar a questão {i}.")
        
        print("\nPronto! Prova 3 populada com 9 questões e pronta para a simulação de desempenho.")
    else:
        print("Erro: Não foi possível gerar a Prova 3.")

    print("proxima etapa, avaliação")

    id_aluno = 1  # aluno_ti_2026 criado na etapa anterior
    id_prova = 3  # Prova "Teste " com 9 questões
    
    # Respostas fornecidas pelo aluno no seu exemplo (Acerta 5 questões: posições 0, 2, 3, 4 e 7)
    respostas_estudante = [2, 3, 2, 2, 2, 4, 1, 2, 3]
    
    print("Iniciando correção automática do simulado...")
    gerar_resultado(
        id_da_prova=id_prova, 
        id_do_estudante=id_aluno, 
        lista_respostas=respostas_estudante
    )
