from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.post_form import PostForm
from forms.category_form import CategoryForm
from forms.post_category_form import PostCategoryForm
# import plotly
from plotly import utils
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func


app = Flask(__name__)
app.secret_key = 'key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/Anna'
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Anna:1998@localhost/Anna'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gnvevljnfcbiaz:cace1e8973298ea0dd74b6683d53b21beae40719fd8b8473b9861e8cd51de8d0@ec2-54-83-9-169.compute-1.amazonaws.com:5432/dedj5aup7544l5'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.String(1000), nullable=False)
    post_hashtag = db.Column(db.String(20), nullable=False)

    Post_Category_Post = db.relationship("Category", secondary='category_post')


class Category(db.Model):
    __tablename__ = 'category'

    name = db.Column(db.String(120), primary_key=True)
    tags = db.Column(db.String(100), nullable=False)
    count_of_subscribers = db.Column(db.Integer, nullable=False)
    comment=  db.Column(db.String(1000), nullable=False)

    Category_Category_Post = db.relationship("Post", secondary='category_post')


class Category_Post(db.Model):
    __tablename__ = 'category_post'

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
    name = db.Column(db.String, db.ForeignKey('category.name'), primary_key=True)





'''
db.create_all()
Entertainment = Category(name= "Entertainment",
          tags  = "travel",
                         count_of_subscribers=2,
                         comment="super")
Beauty = Category(name="Beauty",
          tags  ="health",
                         count_of_subscribers =7,
                         comment="very good")
Literature = Category(name= "Literature",
          tags  = "culture",
                         count_of_subscribers =9,
                         comment="cool")

New_tour = Post(post_id=1,
              post_content="New_tour",
              post_hashtag="#tour")

New_nails = Post(post_id=2,
              post_content="New_nails",
              post_hashtag="#nails")

Old_book = Post(post_id=3,
              post_content="Old_book",
              post_hashtag="#book")
Entertainment.Category_Category_Post.append(New_tour)
Beauty.Category_Category_Post.append(New_nails)
Literature.Category_Category_Post.append(Old_book)

db.session.add_all([Entertainment, Beauty, Literature, New_tour, New_nails, Old_book])
db.session.commit()
'''
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/post', methods=['GET'])
def post():

    result = db.session.query(Post).all()

    return render_template('post.html', posts = result)


@app.route('/categorypost', methods=['GET'])
def categorypost():

    result = db.session.query(Category_Post).all()

    return render_template('categorypost.html', categoryposts = result)


@app.route('/new_user', methods=['GET','POST'])
def new_post():

    form = PostForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('post_form.html', form=form, form_name="New post", action="new_post")
        else:
            new_post = Post(
                                post_id=form.user_id.data
                            )

            db.session.add(new_post)
            db.session.commit()


            return redirect(url_for('post'))

    return render_template('post_form.html', form=form, form_name="New post", action="new_post")



@app.route('/edit_post', methods=['GET','POST'])
def edit_post():

    form = PostForm()


    if request.method == 'GET':

        post_id =request.args.get('post_id')
        post = db.session.query(Post).filter(Post.post_id == post_id).one()

        # fill form and send to user
        form.post_id.data = post.post_id


        return render_template('post_form.html', form=form, form_name="Edit post", action="edit_post")


    else:

        if form.validate() != False:
            return render_template('post_form.html', form=form, form_name="Edit post", action="edit_post")
        else:
            # find user
            post = db.session.query(Post).filter(Post.post_id == form.post_id.data).one()

            # update fields from form data
            post.post_id = form.post_id.data


            db.session.commit()

            return redirect(url_for('post'))



@app.route('/get', methods=['GET'])
def get():
    db.create_all()

    db.session.query(Post).delete()
    db.session.query(Category).delete()
    db.session.query(Category_Post).delete()

    Entertainment = Category(name="Entertainment",
                             tags="travel",
                             count_of_subscribers=2,
                             comment="super")
    Beauty = Category(name="Beauty",
                      tags="health",
                      count_of_subscribers=7,
                      comment="very good")
    Literature = Category(name="Literature",
                          tags="culture",
                          count_of_subscribers=9,
                          comment="cool")

    New_tour = Post(post_id=1,
                    post_content="New_tour",
                    post_hashtag="#tour")

    New_nails = Post(post_id=2,
                     post_content="New_nails",
                     post_hashtag="#nails")

    Old_book = Post(post_id=3,
                    post_content="Old_book",
                    post_hashtag="#book")

    Entertainment.Category_Category_Post.append(New_tour)
    Beauty.Category_Category_Post.append(New_nails)
    Literature.Category_Category_Post.append(Old_book)

    db.session.add_all([Entertainment, Beauty, Literature, New_tour, New_nails, Old_book])
    db.session.commit()

    return redirect(url_for('categorypost'))



@app.route('/show', methods=['GET'])
def show():

    result = db.session.query(Category).all()

    return render_template('category.html', categorys = result)


@app.route('/new_category', methods=['GET','POST'])
def new_category():

    form = CategoryForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('category_form.html', form=form, form_name="New category", action="new_category")
        else:
            new_category= Category(name= form.name.data,
                        tags  =form.tags.data,
                         count_of_subscribers=form.count_of_subscribers.data,
                         comment=form.comment.data
                            )

            db.session.add(new_category)
            db.session.commit()


            return redirect(url_for('show'))

    return render_template('category_form.html', form=form, form_name="New category", action="new_category")









@app.route('/plotly', methods=['GET', 'POST'])
def plotly():
    print("")
    query1 = (
        db.session.query(
            Category.name,
            Category.count_of_subscribers
        )
    ).all()

    # query2 = (
    #     db.session.query(
    #         Category.name,
    #         func.count(Category.post_id).label('category_count')
    #     ).
    #         outerjoin(Category_Post).
    #         group_by(Category.name)
    # ).all()

    name, count = zip(*query1)
    bar = go.Bar(
        x=name,
        y=count
    )

    # name, hashtag_count = zip(*query2)
    # pie = go.Pie(
    #     labels=name,
    #     values=hashtag_count
    # )

    data = {
        "bar": [bar],
        # "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)

if __name__ == "__main__":

    app.run()