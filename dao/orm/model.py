from main import db


class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.String(1000), nullable=False)
    post_hashtag = db.Column(db.String(20), nullable=False)

    Post_Category_Post = db.relationship("Category", secondary='category_post')





class Category_Post(db.Model):
    __tablename__ = 'category_post'

    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)
    name = db.Column(db.String, db.ForeignKey('category.name'), primary_key=True)




class Category(db.Model):
    __tablename__ = 'category'

    name = db.Column(db.String(120), primary_key=True)
    tags = db.Column(db.String(100), nullable=False)
    count_of_subscribers = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000), nullable=False)

    Category_Category_Post = db.relationship("Post", secondary='category_post')
