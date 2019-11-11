
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import CSRFProtect

from forms.forms import TestForm, QuestionForm, QuestionVariantForm, TagForm
from dao.orm.model import *
from dao.db import PostgresDB
from sqlalchemy.sql import func

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import json
app = Flask(__name__)
app.secret_key = 'development key'
csrf = CSRFProtect(app)
db = PostgresDB()


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/test', methods=['GET'])
def test():

    result = db.sqlalchemy_session.query(ormTest).all()

    return render_template('test.html', tests=result)


@app.route('/test', methods=['POST'])
def create_test():
    form = TestForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        db.sqlalchemy_session.add(ormTest(test_name=data.get('test_name'), test_variant=int(data.get('test_variant'))))
        db.sqlalchemy_session.commit()
    return redirect('/test')


@app.route('/test/<id>', methods=['POST'])
def update_test(id):
    form = TestForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        test = db.sqlalchemy_session.query(ormTest).filter(ormTest.test_id == id).first()
        if test:
            test.test_name = data.get('test_name', test.test_name)
            test.test_variant = data.get('test_variant', test.test_variant)
            db.sqlalchemy_session.commit()
            return redirect('/test')
        else:
            return 404


@app.route('/test/<id>/delete', methods=['GET', ])
def delete_test(id):
    test = db.sqlalchemy_session.query(ormTest).filter(ormTest.test_id == id).first()
    db.sqlalchemy_session.delete(test)
    return redirect('/test')


@app.route('/questions', methods=['GET'])
def questions():

    result = db.sqlalchemy_session.query(ormTest).join(ormQuestion).all()

    return render_template('questions.html', tests=result)


@app.route('/question', methods=['POST'])
def create_question():
    form = QuestionForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        db.sqlalchemy_session.add(ormQuestion(question_text=data.get('question_text'), test_id=int(data.get('test_id'))))
        db.sqlalchemy_session.commit()
        return redirect('/questions')
    else:
        return 'errors'


@app.route('/question/<id>', methods=['POST'])
def update_question(id):
    form = QuestionForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        question = db.sqlalchemy_session.query(ormQuestion).filter(ormQuestion.question_id == id).first()
        if question:
            question.question_text = data.get('question_text', question.question_text)
            db.sqlalchemy_session.commit()
            return redirect('/questions')
        else:
            return 'errors'


@app.route('/question/<id>/delete', methods=['GET', ])
def delete_question(id):
    question = db.sqlalchemy_session.query(ormQuestion).filter(ormQuestion.question_id == id).first()
    db.sqlalchemy_session.delete(question)
    return redirect('/questions')


@app.route('/question_variants', methods=['GET'])
def question_variants():

    result = db.sqlalchemy_session.query(ormQuestion).join(ormQuestionVariant).all()

    return render_template('question_variants.html', questions=result)


@app.route('/question_variant', methods=['POST'])
def create_question_variant():
    form = QuestionVariantForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        db.sqlalchemy_session.add(ormQuestionVariant(answer_variant_text=data.get('answer_variant_text'), question_id=int(data.get('question_id'))))
        db.sqlalchemy_session.commit()
        return redirect('/question_variants')
    else:
        return 'errors'


@app.route('/question_variant/<id>', methods=['POST'])
def update_answer_variant(id):
    form = QuestionVariantForm(request.form)
    data = dict(request.form)
    data.pop('csrf_token', None)
    if form.validate():
        answer_variant = db.sqlalchemy_session.query(ormQuestionVariant).filter(ormQuestionVariant.answer_variant_id == id).first()
        if answer_variant:
            answer_variant.answer_variant_text = data.get('answer_variant_text', answer_variant.answer_variant_text)
            db.sqlalchemy_session.commit()
            return redirect('/question_variants')
        else:
            return 'errors'


@app.route('/question_variants/<id>/delete', methods=['GET', ])
def delete_question_variants(id):
    db.sqlalchemy_session.query(ormQuestionVariant).filter(ormQuestionVariant.answer_variant_id == id).delete(synchronize_session='evaluate')
    db.sqlalchemy_session.commit()
    return redirect('/question_variants')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    query1 = db.sqlalchemy_session.query(
        ormTest.test_name,
        func.count(ormTest.test_variant).label('test_variants_count')).group_by(
        ormTest.test_name
    )

    query2 = db.sqlalchemy_session.query(
        ormTest.test_name,
        func.count(ormQuestion.question_id).label('question_count')
    ).outerjoin(ormQuestion).group_by(ormTest.test_name).all()

    query3 = db.sqlalchemy_session.query(
        ormTag.tag_category,
        func.count(ormTag.count_of_likes).label('likes_amount')
    ).outerjoin(ormQuestion).group_by(ormTag.tag_category).all()

    variants, question_counts = zip(*query1)
    bar = go.Bar(
        x=variants,
        y=question_counts
    )

    tests, question_count = zip(*query2)
    pie = go.Pie(
        labels=tests,
        values=question_count
    )

    category, likes_amount = zip(*query3)
    bar_second = go.Bar(
        x=category,
        y=likes_amount
)
    data = {
        "bar":[bar,bar_second],
        "pie":[pie]
    }
    graphsJSON = json.dumps(
        data,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/get', methods=['GET', ])
def get():
    db.sqlalchemy_session.query(ormTag).insert(
        tag_name='first',
        tag_category ='asfas',
        count_of_likes=10,
        count_of_dislikes=2,
        question_id=1
    )
    db.sqlalchemy_session.query(ormTag).insert(
        tag_name='second',
        tag_category ='pofjf',
        count_of_likes=20,
        count_of_dislikes=4,
        question_id=2
    )
    db.sqlalchemy_session.query(ormTag).insert(
        tag_name='third',
        tag_category ='wgdhjf',
        count_of_likes=15,
        count_of_dislikes=5,
        question_id=3
    )
    db.sqlalchemy_session.commit()
    return 'Created', 201

@app.route('/show', methods=['GET', ])
def show():
    result = db.sqlalchemy_session.query(ormTag).all()
    return render_template('tag.html', tags=result)

@app.route('/update', methods=['POST', ])
def update():
    data = request.form
    form = TagForm(data)
    if not form.validate():
        return render_template('tag.html', errors=form.errors)
    db.sqlalchemy_session.add(ormTag(tag_category=data.get('tag_category'), count_of_likes=int(data.get('count_of_likes'))))
    db.sqlalchemy_engine.commit()
    return render_template('tag.html')

if __name__ == '__main__':
    app.run(debug=True)
