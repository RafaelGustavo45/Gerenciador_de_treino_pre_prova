import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

@pytest.fixture
pyt_test_db = os.path.join(tempfile.gettempdir(), 'banco_testes.sqlite')

@pytest.fixture
def app():
    if os.path.exists(pyt_test_db):
        os.remove(pyt_test_db)
        
    app = create_app({
        'TESTING': True,
        'DATABASE': pyt_test_db,
    })

    with app.app_context():
        init_db()
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?);",
            ('admin_teste', 'pbkdf2:sha256:600000$fakehash', 1)
        )
        db.commit()

    yield app

    if os.path.exists(pyt_test_db):
        os.remove(pyt_test_db)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    class AuthActions:
        def login(self, username='admin_teste', password='123'):
            return client.post('/auth/login', data={'username': username, 'password': password})

        def logout(self):
            return client.get('/auth/logout')

    return AuthActions()

def test_1_criacao_prova(client, auth):
    auth.login()
    response = client.post('/create', data={
        'titulo': 'prova teste 1',
        'serie': '8',
        'materia': 'historia'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    with client.application.app_context():
        db = get_db()
        prova = db.execute('SELECT * FROM provas WHERE id = 1').fetchone()
        assert prova is not None
        assert prova['titulo'] == 'prova teste 1'
        assert prova['serie'] == '8'
        assert prova['materia'] == 'historia'

def test_2_update_prova(client, auth):
    auth.login()
    client.post('/create', data={
        'titulo': 'prova teste 1',
        'serie': '8',
        'materia': 'historia'
    })
    
    response = client.post('/1/update', data={
        'titulo': 'prova teste update',
        'serie': '9',
        'materia': 'biologia'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    with client.application.app_context():
        db = get_db()
        prova = db.execute('SELECT * FROM provas WHERE id = 1').fetchone()
        assert prova['titulo'] == 'prova teste update'
        assert prova['serie'] == '9'
        assert prova['materia'] == 'biologia'

def test_3_criacao_e_delete_prova(client, auth):
    auth.login()
    client.post('/create', data={
        'titulo': 'prova para deletar',
        'serie': '1',
        'materia': 'teste'
    })
    
    with client.application.app_context():
        db = get_db()
        prova = db.execute('SELECT * FROM provas WHERE id = 1').fetchone()
        assert prova is not None

    response = client.post('/1/delete', follow_redirects=True)
    assert response.status_code == 200

    with client.application.app_context():
        db = get_db()
        prova = db.execute('SELECT * FROM provas WHERE id = 1').fetchone()
        assert prova is None

def test_4_criacao_update_delete_questao(client, auth):
    auth.login()
    client.post('/create', data={
        'titulo': 'Prova Questões',
        'serie': '5',
        'materia': 'Ciências'
    })

    response = client.post('/prova/1/questao/create', data={
        'enunciados[]': ['0'],
        'questoes[0][enunciado]': 'Qual a capital do Brasil?',
        'questoes[0][alternativas][]': ['São Paulo', 'Brasília', 'Rio de Janeiro'],
        'questoes[0][correta]': '1'
    }, follow_redirects=True)
    
    assert response.status_code == 200

    with client.application.app_context():
        db = get_db()
        questao = db.execute('SELECT * FROM questoes WHERE id = 1').fetchone()
        assert questao is not None
        assert questao['enunciado'] == 'Qual a capital do Brasil?'
        assert questao['resposta'] == 'Brasília'

    response_update = client.post('/questao/1/update', data={
        'enunciado': 'Qual a capital da França?',
        'alternativas[]': ['Londres', 'Paris', 'Berlim'],
        'alternativa_correta': '1'
    }, follow_redirects=True)
    
    assert response_update.status_code == 200

    with client.application.app_context():
        db = get_db()
        questao_up = db.execute('SELECT * FROM questoes WHERE id = 1').fetchone()
        assert questao_up['enunciado'] == 'Qual a capital da França?'
        assert questao_up['resposta'] == 'Paris'

    response_delete = client.post('/questao/1/delete', follow_redirects=True)
    assert response_delete.status_code == 200

    with client.application.app_context():
        db = get_db()
        questao_del = db.execute('SELECT * FROM questoes WHERE id = 1').fetchone()
        assert questao_del is None

def test_5_criacao_update_delete_alternativa(client, auth):
    auth.login()
    client.post('/create', data={
        'titulo': 'Prova Alternativas',
        'serie': '6',
        'materia': 'Geografia'
    })

    client.post('/prova/1/questao/create', data={
        'enunciados[]': ['0'],
        'questoes[0][enunciado]': 'Maior oceano?',
        'questoes[0][alternativas][]': ['Atlântico', 'Pacífico'],
        'questoes[0][correta]': '1'
    })

    with client.application.app_context():
        db = get_db()
        alts = db.execute('SELECT * FROM questoes_alternativas WHERE questao_id_fk = 1').fetchall()
        assert len(alts) == 2
        assert alts[1]['alternativa'] == 'Pacífico'
        assert alts[1]['is_correct'] == 1

    client.post('/questao/1/update', data={
        'enunciado': 'Maior oceano?',
        'alternativas[]': ['Índico', 'Ártico', 'Pacífico'],
        'alternativa_correta': '2'
    })

    with client.application.app_context():
        db = get_db()
        alts_up = db.execute('SELECT * FROM questoes_alternativas WHERE questao_id_fk = 1 ORDER BY id ASC').fetchall()
        assert len(alts_up) == 3
        assert alts_up[0]['alternativa'] == 'Índico'
        assert alts_up[2]['alternativa'] == 'Pacífico'
        assert alts_up[2]['is_correct'] == 1

    client.post('/questao/1/delete', follow_redirects=True)

    with client.application.app_context():
        db = get_db()
        alts_del = db.execute('SELECT * FROM questoes_alternativas WHERE questao_id_fk = 1').fetchall()
        assert len(alts_del) == 0