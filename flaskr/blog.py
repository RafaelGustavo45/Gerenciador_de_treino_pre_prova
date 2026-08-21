# flaskr/blog.py
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, abort
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    provas = db.execute(
        'SELECT p.id, titulo, materia, serie, created, author_id_fk, username'
        ' FROM provas p JOIN user u ON p.author_id_fk = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', provas=provas)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        materia = request.form['materia']
        serie = request.form['serie']
        error = None

        if not titulo:
            error = 'Título é obrigatório.'

        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO provas (titulo, materia, serie, author_id_fk) VALUES (?, ?, ?, ?)',
                (titulo, materia, serie, g.user['id'])
            )
            db.commit()
            flash('Prova criada com sucesso!', 'success')
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_prova(id, check_author=True):
    prova = get_db().execute(
        'SELECT p.id, titulo, serie, materia, author_id_fk, username'
        ' FROM provas p JOIN user u ON p.author_id_fk = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if prova is None:
        abort(404, f"Prova id {id} não existe.")

    if check_author and g.user['is_admin'] == 0 and prova['author_id_fk'] != g.user['id']:
        abort(403)

    return prova

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    prova = get_prova(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        serie = request.form['serie']
        materia = request.form['materia']
        error = None

        if not titulo:
            error = 'Título é obrigatório.'

        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'UPDATE provas SET titulo = ?, serie = ?, materia = ? WHERE id = ?',
                (titulo, serie, materia, id)
            )
            db.commit()
            flash('Prova atualizada!', 'success')
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', prova=prova)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_prova(id)
    db = get_db()
    db.execute('DELETE FROM provas WHERE id = ?', (id,))
    db.commit()
    flash('Prova deletada.', 'success')
    return redirect(url_for('blog.index'))


# --- ROTAS DE QUESTÕES E ALTERNATIVAS ---

def get_questao(id, check_author=True):
    questao = get_db().execute(
        'SELECT q.id, q.prova_id_fk, q.enunciado, q.resposta, p.author_id_fk'
        ' FROM questoes q JOIN provas p ON q.prova_id_fk = p.id'
        ' WHERE q.id = ?',
        (id,)
    ).fetchone()

    if questao is None:
        abort(404, f"Questão id {id} não existe.")

    if check_author and g.user['is_admin'] == 0 and questao['author_id_fk'] != g.user['id']:
        abort(403)

    return questao

@bp.route('/prova/<int:prova_id>/questoes')
def listar_questoes(prova_id):
    prova = get_prova(prova_id, check_author=False)
    db = get_db()
    questoes = db.execute(
        'SELECT id, prova_id_fk, enunciado, resposta, created'
        ' FROM questoes'
        ' WHERE prova_id_fk = ?'
        ' ORDER BY created ASC',
        (prova_id,)
    ).fetchall()
    
    # Opcional: Buscar alternativas de cada questão para exibir na tela se necessário
    return render_template('blog/questoes.html', prova=prova, questoes=questoes)

@bp.route('/prova/<int:prova_id>/questao/create', methods=('GET', 'POST'))
@login_required
def create_questao(prova_id):
    prova = get_prova(prova_id)
    if request.method == 'POST':
        # Captura as listas enviadas pelo formulário dinâmico
        enunciados = request.form.getlist('enunciados[]')
        
        error = None
        if not enunciados or len(enunciados) == 0:
            error = 'Nenhuma questão foi informada.'

        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            
            # Como podemos ter múltiplas questões geradas de uma vez:
            for q_index in range(len(enunciados)):
                enunciado = request.form.get(f'questoes[{q_index}][enunciado]')
                alternativas = request.form.getlist(f'questoes[{q_index}][alternativas][]')
                correta_index = request.form.get(f'questoes[{q_index}][correta]', type=int)

                if not enunciado or not enunciado.strip():
                    continue

                if len(alternativas) < 2:
                    continue

                # Define o gabarito como sendo o texto da alternativa correta
                texto_resposta_correta = alternativas[correta_index] if (correta_index is not None and 0 <= correta_index < len(alternativas)) else alternativas[0]

                # Insere a questão
                cursor = db.execute(
                    'INSERT INTO questoes (prova_id_fk, enunciado, resposta) VALUES (?, ?, ?)',
                    (prova_id, enunciado, texto_resposta_correta)
                )
                questao_id = cursor.lastrowid

                # Insere as alternativas
                for index, alt_texto in enumerate(alternativas):
                    if alt_texto.strip():
                        is_correct = 1 if index == correta_index else 0
                        db.execute(
                            'INSERT INTO questoes_alternativas (questao_id_fk, alternativa, is_correct) VALUES (?, ?, ?)',
                            (questao_id, alt_texto, is_correct)
                        )

            db.commit()
            flash('Questões adicionadas com sucesso!', 'success')
            return redirect(url_for('blog.listar_questoes', prova_id=prova_id))
            
    return render_template('blog/create_questao.html', prova=prova)

@bp.route('/questao/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_questao(id):
    questao = get_questao(id)
    db = get_db()
    
    if request.method == 'POST':
        enunciado = request.form['enunciado']
        alternativas = request.form.getlist('alternativas[]')
        correta_index = request.form.get('alternativa_correta', type=int)
        
        error = None
        
        if not enunciado:
            error = 'O enunciado é obrigatório.'
        elif len(alternativas) < 2:
            error = 'A questão deve ter pelo menos 2 alternativas.'
        elif correta_index is None or correta_index < 0 or correta_index >= len(alternativas):
            error = 'Você deve selecionar exatamente uma alternativa correta.'
            
        if error is not None:
            flash(error, 'error')
        else:
            # Define o texto da resposta correta automaticamente com base na alternativa selecionada
            resposta_correta_texto = alternativas[correta_index]

            db.execute(
                'UPDATE questoes SET enunciado = ?, resposta = ? WHERE id = ?',
                (enunciado, resposta_correta_texto, id)
            )
            
            # Atualiza alternativas (remove antigas e insere as novas)
            db.execute('DELETE FROM questoes_alternativas WHERE questao_id_fk = ?', (id,))
            for index, alt_texto in enumerate(alternativas):
                if alt_texto.strip():
                    is_correct = 1 if index == correta_index else 0
                    db.execute(
                        'INSERT INTO questoes_alternativas (questao_id_fk, alternativa, is_correct) VALUES (?, ?, ?)',
                        (id, alt_texto, is_correct)
                    )

            db.commit()
            flash('Questão atualizada!', 'success')
            return redirect(url_for('blog.listar_questoes', prova_id=questao['prova_id_fk']))
            
    # Busca as alternativas existentes para exibir no template de edição
    alternativas = db.execute(
        'SELECT id, alternativa, is_correct FROM questoes_alternativas WHERE questao_id_fk = ?',
        (id,)
    ).fetchall()

    return render_template('blog/update_questao.html', questao=questao, alternativas=alternativas)

@bp.route('/questao/<int:id>/delete', methods=('POST',))
@login_required
def delete_questao(id):
    questao = get_questao(id)
    prova_id = questao['prova_id_fk']

    db = get_db()
    db.execute('DELETE FROM questoes WHERE id = ?', (id,))
    db.commit()
    flash('Questão excluída com sucesso.', 'success')

    return redirect(url_for('blog.listar_questoes', prova_id=prova_id))

# --- TRATAMENTOS DE ERRO ---
@bp.app_errorhandler(403)
def sem_permissao(error):
    flash('Você não tem permissão para fazer isso!', 'error')
    return redirect(url_for('blog.index'))

@bp.app_errorhandler(404)
def pagina_nao_encontrada(error):
    flash('Página não encontrada.', 'error')
    return redirect(url_for('index'))