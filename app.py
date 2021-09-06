from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    f'DATABASE_URL'.replace('postgres', 'postgresql'))
db = SQLAlchemy(app)


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Code %r>' % self.id


@app.route('/about', methods=['GET'])
def index():
    codes = Code.query.all()
    return render_template('sample.html', codes=codes)


@app.route('/', methods=['GET', 'POST'])
def post():
    if request.method != 'POST':
        return render_template('form.html')
    code = request.form['code']
    if code:
        try:
            code_db = Code(code=code, uuid=str(uuid.uuid4()))
            db.session.add(code_db)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error')
    return redirect(f'/{code_db.uuid}')


@app.route('/<id>', methods=['GET'])
def code_text(id):
    code = Code.query.filter_by(uuid=id).first_or_404(
        description='There is no data with id {}'.format(id))
    # code = Code.query.filter_by(uuid=id).first()
    return render_template('index.html', code=code, length=len(code.code.split('\n')))


@app.route('/raw/<id>', methods=['GET'])
def code_raw(id):
    code = Code.query.filter_by(uuid=id).first()
    return render_template('raw.html', code=code)


@app.route('/duplicate/<id>', methods=['GET', 'POST'])
def duplicate_post(id):
    if request.method == 'GET':
        code_id = id.replace('%7D', '').replace('}', '')
        print(code_id)
        codes = Code.query.get(code_id)
        return render_template('form.html', value=codes)
    code = request.form['code']
    if code:
        try:
            code_db = Code(code=code, uuid=str(uuid.uuid4()))
            db.session.add(code_db)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error')
    return redirect(f'/{code_db.uuid}')


if __name__ == '__main__':
    app.run(host='https://haste-bin-clone.herokuapp.com/')
