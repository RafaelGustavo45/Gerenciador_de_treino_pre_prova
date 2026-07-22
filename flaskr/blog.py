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

    if check_author and prova['author_id'] != g.user['id']:
        abort(403) # Forbidden

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