from dao.orm.model import *

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