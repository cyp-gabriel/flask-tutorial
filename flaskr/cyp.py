import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('cyp', __name__, url_prefix='/cyp')

@bp.route('/applications')
def applications():
    db = get_db()
    applications = db.execute(
        'SELECT id, first_name, last_name FROM application'
    ).fetchall()
    return render_template('cyp/applications.html', applications=applications)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None

        if not first_name:
            error = 'first_name is required.'
        if not last_name:
            error = 'last_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO application (first_name, last_name)'
                ' VALUES (?, ?)',
                (first_name, last_name)
            )
            db.commit()
            return redirect(url_for('cyp.applications'))

    return render_template('cyp/create.html')

def get_application(id):
    application = get_db().execute(
        'SELECT id, first_name, last_name'
        ' FROM application'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if application is None:
        abort(404, f"application id {id} doesn't exist.")


    return application


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    application = get_application(id)

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None

        if not first_name:
            error = 'first_name is required.'
        if not last_name:
            error = 'last_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE application SET first_name = ?, last_name = ?'
                ' WHERE id = ?',
                (first_name, last_name, id)
            )
            db.commit()
            return redirect(url_for('cyp.applications'))

    return render_template('cyp/update.html', application=application)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_application(id)
    db = get_db()
    db.execute('DELETE FROM application WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('cyp.applications'))