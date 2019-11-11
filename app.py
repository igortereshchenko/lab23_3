
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from forms.user_form import StudentForm, DisciplineForm, PostForm, DisciplineForm1, StudentForm1, PostForm1, CategoryForm1


import plotly.graph_objs as go
import plotly
import json

import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'


if ENV == 'dev':
   app.debug = True



else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://eidhbftwuebdku:c8e731c09eced3e0f723295404d5991d0f4b47b64f84f0a2ced174e6c4ddd968@ec2-174-129-253-63.compute-1.amazonaws.com:5432/d26i6lngo5kn5v'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False





db = SQLAlchemy(app)


class ormStudent(db.Model):
    __tablename__ = 'Student'

    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(20))
    student_surname = db.Column(db.String(20), nullable=False)
    student_group = db.Column(db.String(20))
    student_ = db.relationship('ormPost')


class ormPost(db.Model):
    __tablename__ = 'Post'
    post_id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(20) , nullable=False)
    post_text = db.Column(db.String(20),nullable=False)
    stud_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'))
    disc_id = db.Column(db.Integer, db.ForeignKey('Discipline.disc_id'))
    name = db.Column(db.String(20), db.ForeignKey('Category.name'))






class ormDiscipline(db.Model):
    __tablename__ = 'Discipline'

    disc_id = db.Column(db.Integer, primary_key=True)
    disc_name = db.Column(db.String(30))
    disc_type = db.Column(db.String(30))

    student_ = db.relationship('ormPost')


class ormCategory(db.Model):
    __tablename__ = 'Category'
    name = db.Column(db.String(20), primary_key=True)
    age_group = db.Column(db.Integer)
    tags = db.Column(db.String(100))
    count_of_subscribers = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    student_ = db.relationship('ormPost')



'''


db.session.query(ormPost).delete()
db.session.query(ormDiscipline).delete()
db.session.query(ormStudent).delete()


Student1 = ormStudent(student_id=1, student_name='Kate', student_surname='Buch', student_group='ka34')
Student2 = ormStudent(student_id=2, student_name='Vlad', student_surname='Kanevskiy', student_group='km63')
Student3 = ormStudent(student_id=3, student_name='Dima', student_surname='Koltsov', student_group='km61')

Discipline1 = ormDiscipline(disc_id=1, disc_name='matan', disc_type='type1')
Discipline2 = ormDiscipline(disc_id=2, disc_name='la', disc_type='type1')
Discipline3 = ormDiscipline(disc_id=3, disc_name='english', disc_type='type2')

Post1 = ormPost(post_id=1, post_type='advance', post_text='bla', stud_id=1, disc_id=1)
Post2 = ormPost(post_id=2, post_type='complaint', post_text='bla_bla', stud_id=2, disc_id=3)
Post3 = ormPost(post_id=3, post_type='complaint', post_text='bla1', stud_id=1, disc_id=1)



Student1.student_.append(Post1)
Student1.student_.append(Post3)
Student2.student_.append(Post2)

Discipline1.student_.append(Post1)
Discipline3.student_.append(Post2)
Discipline1.student_.append(Post3)


db.session.add_all([Student1, Student2, Student3])
db.session.add_all([Post1, Post2, Post3])
db.session.add_all([Discipline1, Discipline2, Discipline3])
db.session.commit()

'''
#main page
@app.route('/get', methods=['GET'])
def category1():
    db.session.query(ormCategory).delete()



    Category1 = ormCategory(name='category1', age_group='12', tags='tag1, tag2, tag3', count_of_subscribers=3, post_id=1)
    Category2 = ormCategory(name='category2', age_group='40', tags='tag4, tag5, tag3', count_of_subscribers=8, post_id=2)
    Category3 = ormCategory(name='category3', age_group='3', tags='tag1, tag2, tag3', count_of_subscribers=9, post_id=3)


    Post1 = ormPost(post_id=6, post_type='advance', post_text='bla', stud_id=1, disc_id=1, name='category1')
    Post2 = ormPost(post_id=7, post_type='complaint', post_text='bla_bla', stud_id=2, disc_id=3, name='category1')
    Post3 = ormPost(post_id=8, post_type='complaint', post_text='bla1', stud_id=1, disc_id=1, name='category3')





    db.session.add_all([Post1, Post2, Post3])
    db.session.add_all([Category1, Category2, Category3])

    db.session.commit()

    return redirect('/api')

@app.route('/update/<string:x>', methods=['GET','POST'])
def update(x):

    form = CategoryForm1()
    user = db.session.query(ormCategory).filter(ormCategory.name == x).one()

    if request.method == 'GET':



        # fill form and send to user

        form.name.data = user.name
        form.tags.data = user.tags
        form.count_of_subscribers.data = user.count_of_subscribers
        return render_template('category_form1.html', form=form, form_name="Edit category")

    else:

        if form.validate() == False:
            return render_template('category_form1.html', form=form, form_name="Edit category")
        else:
            user.name = form.name.data
            user.tags = form.tags.data
            user.count_of_subscribers = form.count_of_subscribers.data

            db.session.commit()

            return redirect(url_for('category'))


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

@app.route('/api', methods=['GET', 'POST'])
def category():

    result = db.session.query(ormCategory).all()

    return render_template('category.html', category=result)

#hilday pages
@app.route('/student', methods=['GET'])
def student():

    result = db.session.query(ormStudent).all()
    return render_template('student.html', student = result)


@app.route('/new_student', methods=['GET','POST'])
def new_student():

    form = StudentForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            new_user= ormStudent(
                student_id=form. student_id.data,
                student_name=form.student_name.data,
                student_surname=form.student_surname.data,
                student_group=form.student_group.data
                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student/<int:x>', methods=['GET','POST'])
def edit_student(x):

    form = StudentForm1()
    user = db.session.query(ormStudent).filter(ormStudent.student_id == x).one()

    if request.method == 'GET':



        # fill form and send to user

        form.student_name.data = user.student_name
        form.student_surname.data = user.student_surname
        form.student_group.data = user.student_group
        return render_template('student_form1.html', form=form, form_name="Edit student")

    else:

        if form.validate() == False:
            return render_template('student_form1.html', form=form, form_name="Edit student")
        else:
            user.student_name = form.student_name.data
            user.student_surname = form.student_surname.data
            user.student_group = form.student_group.data

            db.session.commit()

            return redirect(url_for('student'))

@app.route('/delete_student/<int:x>', methods=['GET'])
def delete_student(x):
    result = db.session.query(ormStudent).filter(ormStudent.student_id == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('succ.html')


#client
@app.route('/post', methods=['GET'])
def post():

    result = db.session.query(ormPost).all()

    return render_template('post.html', post = result)


@app.route('/new_post', methods=['GET','POST'])
def new_post():

    form = PostForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('post_form.html', form=form, form_name="New post", action="new_post")
        else:
            new_user = ormPost(
                post_id=form.post_id.data,
                post_type=form.post_type.data,
                post_text=form.post_text.data,
                stud_id=form.stud_id.data,
                disc_id=form.disc_id.data,

                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('post'))

    return render_template('post_form.html', form=form, form_name="New post", action="new_post")

@app.route('/edit_post/<int:x>', methods=['GET','POST'])
def edit_post(x):

    form = PostForm1()

    user = db.session.query(ormPost).filter(ormPost.post_id == x).one()

    if request.method == 'GET':

        #user_id =request.args.get('post_id')


        # fill form and send to user

        form.post_text.data = user.post_text
        form.post_type.data =user.post_type
        form.stud_id.data = user.stud_id
        form.disc_id.data = user.disc_id

        return render_template('post_form1.html', form=form, form_name="Edit post")


    else:

        if form.validate() == False:
            return render_template('post_form1.html', form=form, form_name="Edit post")
        else:

            # find user

            # update fields from form data
            user.post_text = form.post_text.data
            user.post_type = form.post_type.data
            user.stud_id = form.stud_id.data
            user.disc_id = form.disc_id.data

            db.session.commit()

            return redirect(url_for('post'))


@app.route('/delete_post/<int:x>', methods=['GET'])
def delete_post(x):

    #user_id = request.form['post_id']


    result = db.session.query(ormPost).filter(ormPost.post_id ==x).one()

    db.session.delete(result)
    db.session.commit()


    return render_template('succ.html')


#presents pages
@app.route('/discipline', methods=['GET'])
def discipline():

    result = db.session.query(ormDiscipline).all()

    return render_template('discipline.html', discipline = result)


@app.route('/new_discipline', methods=['GET','POST'])
def new_discipline():

    form = DisciplineForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")
        else:
            new_user = ormDiscipline(
                disc_id=form.disc_id.data,
                disc_type=form.disc_type.data,
                disc_name=form.disc_name.data,

                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")

@app.route('/edit_discipline/<int:x>', methods=['GET','POST'])
def edit_discipline(x):

    form = DisciplineForm1()

    user = db.session.query(ormDiscipline).filter(ormDiscipline.disc_id == x).one()

    if request.method == 'GET':



        form.disc_name.data = user.disc_name
        form.disc_type.data =user.disc_type


        return render_template('discipline_form1.html', form=form, form_name="Edit disc")


    else:

        if form.validate() == False:
            return render_template('discipline_form1.html', form=form, form_name="Edit disc")
        else:

            # find user

            # update fields from form data
            user.disc_name = form.disc_name.data
            user.disc_type = form.disc_type.data


            db.session.commit()

            return redirect(url_for('discipline'))


@app.route('/delete_discipline/<int:x>', methods=['GET'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    query1 = (
        db.session.query(
            ormDiscipline.disc_type,
            func.count(ormPost.post_id).label('post')
        ).
            outerjoin(ormPost).
            group_by(ormDiscipline.disc_type)
    ).all()

    query2 = (
        db.session.query(
            ormStudent.student_group,
            func.count(ormPost.post_id).label('...')
        ).
            outerjoin(ormPost).
            group_by(ormStudent.student_group)
    ).all()


    names, skill_counts = zip(*query1)
    bar = go.Bar(
        x=names,
        y=skill_counts
    )

    skills, user_count = zip(*query2)
    pie = go.Pie(
        labels=skills,
        values=user_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]

    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/plot', methods=['GET', 'POST'])
def dashboard1():

    query1 = (
        db.session.query(
            ormCategory.name,
            func.count(ormCategory.post_id)
        ).group_by(ormCategory.name)

    ).all()






    names, skill_counts = zip(*query1)
    bar = go.Bar(
        x=names,
        y=skill_counts
    )


    data = {
        "bar": [bar]


    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphsJSON=graphsJSON)


if __name__ == '__main__':
    app.run(debug=True)