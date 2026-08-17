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
        'SELECT p.id, titulo, materia, serie, created, author_id, username'
        ' FROM provas p JOIN user u ON p.author_id = u.id'
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
                'INSERT INTO provas (titulo, materia, serie, author_id) VALUES (?, ?, ?, ?)',
                (titulo, materia, serie ,g.user['id'])
            )
            db.commit()
            flash('Prova criada com sucesso!', 'success')
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_prova(id, check_author=True):
    """Função auxiliar para buscar uma prova e garantir que ele existe."""
    prova = get_db().execute(
        'SELECT p.id, titulo, serie, materia, author_id, username'
        ' FROM provas p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if prova is None:
        abort(404, f"Prova id {id} não existe.")

        # Se não for admin E não for o dono da prova, bloqueia
    if check_author and g.user['is_admin'] == 0 and prova['author_id'] != g.user['id']:
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
            flash('Prova atualizadoa!', 'success')
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', prova=prova)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_prova(id) # Garante que a prova existe e o usuário é o autor
    db = get_db()
    db.execute('DELETE FROM provas WHERE id = ?', (id,))
    db.commit()
    flash('Prova deletada.', 'success')
    return redirect(url_for('blog.index'))


# ROTAS DE QUESTÕES (ADICIONADAS)

def get_questao(id, check_author=True):
    questao = get_db().execute(
        'SELECT q.id, q.prova_id, q.enunciado, q.resposta, p.author_id'
        ' FROM questoes q JOIN provas p ON q.prova_id = p.id'
        ' WHERE q.id = ?',
        (id,)
    ).fetchone()


    if questao is None:
        abort(404, f"Questão id {id} não existe.")

    if check_author and g.user['is_admin'] == 0 and questao['author_id'] != g.user['id']:
        abort(403)

    return questao

@bp.route('/prova/<int:prova_id>/questoes')
def listar_questoes(prova_id):
    prova = get_prova(prova_id, check_author=False)
    db = get_db()
    questoes = db.execute(
        'SELECT id, prova_id, enunciado, resposta, created'
        ' FROM questoes'
        ' WHERE prova_id = ?'
        ' ORDER BY created ASC',
        (prova_id,)
    ).fetchall()
    return render_template('blog/questoes.html', prova=prova, questoes=questoes)

@bp.route('/prova/<int:prova_id>/questao/create', methods=('GET', 'POST'))
@login_required
def create_questao(prova_id):
    prova = get_prova(prova_id)
    if request.method == 'POST':
        enunciado = request.form['enunciado']
        resposta = request.form['resposta'] # Captura o gabarito
        error = None
        
        if not enunciado:
            error = 'O enunciado da questão é obrigatório.'
        elif not resposta:
            error = 'A resposta da questão é obrigatória.'
            
        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO questoes (prova_id, enunciado, resposta) VALUES (?, ?, ?)',
                (prova_id, enunciado, resposta)
            )
            db.commit()
            flash('Questão adicionada com sucesso!', 'success')
            return redirect(url_for('blog.listar_questoes', prova_id=prova_id))
    return render_template('blog/create_questao.html', prova=prova)

@bp.route('/questao/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_questao(id):
    questao = get_questao(id)
    if request.method == 'POST':
        enunciado = request.form['enunciado']
        resposta = request.form['resposta']
        error = None
        
        if not enunciado:
            error = 'O enunciado é obrigatório.'
        elif not resposta:
            error = 'A resposta é obrigatória.'
            
        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'UPDATE questoes SET enunciado = ?, resposta = ? WHERE id = ?',
                (enunciado, resposta, id)
            )
            db.commit()
            flash('Questão atualizada!', 'success')
            return redirect(url_for('blog.listar_questoes', prova_id=questao['prova_id']))
    return render_template('blog/update_questao.html', questao=questao)

@bp.route('/questao/<int:id>/delete', methods=('POST',))
@login_required
def delete_questao(id):
    """Deleta uma questão."""
    questao = get_questao(id)
    prova_id = questao['prova_id']

    db = get_db()
    db.execute('DELETE FROM questoes WHERE id = ?', (id,))
    db.commit()
    flash('Questão excluída com sucesso.', 'success')

    return redirect(url_for('blog.listar_questoes', prova_id=prova_id))

# --- TRATAMENTO AMIGÁVEL PARA USUÁRIO SEM PERMISSÃO ---
@bp.app_errorhandler(403)
def sem_permissao(error):
    flash(' Você não tem permissão para fazer isso!', 'error')
    return redirect(url_for('blog.index'))

@bp.app_errorhandler(404)
def pagina_nao_encontrada(error):
    flash('Página não encontrada.', 'error')
    return redirect(url_for('blog.index'))
