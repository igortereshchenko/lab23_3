from dao.orm.model import *
from dao.db import PostgresDB

db = PostgresDB()

Base.metadata.create_all(db.sqlalchemy_engine)


session = db.sqlalchemy_session

session.query(ormQuestionVariant).delete()
session.query(ormQuestion).delete()
session.query(ormTest).delete()
session.query(ormTag).delete()

test_1_v_1 = ormTest(
    # test_id=1,
    test_name='First test',
    test_variant=1,
)

test_1_v_2 = ormTest(
    # test_id=2,
    test_name='First test',
    test_variant=2,
)

test_1_v_3 = ormTest(
    # test_id=3,
    test_name='First test',
    test_variant=3,
)

test_2_v_1 = ormTest(
    # test_id=4,
    test_name='Second test',
    test_variant=1,
)

session.add_all([
    test_1_v_1, test_1_v_2, test_1_v_3, test_2_v_1,
])
session.commit()

test_1_v_1_question_1 = ormQuestion(
    # question_id=1,
    question_text='How are u?',
    test_id=test_1_v_1.test_id,
)

test_1_v_1_question_2 = ormQuestion(
    # question_id=2,
    question_text='What is your name?',
    test_id=test_1_v_1.test_id,
)

test_1_v_1_question_3 = ormQuestion(
    # question_id=3,
    question_text='How old are you?',
    test_id=test_1_v_1.test_id,
)

test_1_v_2_question_1 = ormQuestion(
    # question_id=4,
    question_text='What is your favourite color?',
    test_id=test_1_v_1.test_id,
)

session.add_all([
    test_1_v_1_question_1, test_1_v_1_question_2, test_1_v_1_question_3, test_1_v_2_question_1,
])
session.commit()

test_1_v_1_question_1_variant_1 = ormQuestionVariant(
    # answer_variant_id=1,
    answer_variant_text='Fine',
    question_id=test_1_v_1_question_1.question_id
)

test_1_v_1_question_1_variant_2 = ormQuestionVariant(
    # answer_variant_id=2,
    answer_variant_text='Bad',
    question_id=test_1_v_1_question_1.question_id,
    answer_check=True
)

test_1_v_1_question_1_variant_3 = ormQuestionVariant(
    # answer_variant_id=3,
    answer_variant_text='so-so',
    question_id=test_1_v_1_question_1.question_id
)

test_1_v_1_question_2_variant_1 = ormQuestionVariant(
    # answer_variant_id=4,
    answer_variant_text='Hanna',
    question_id=test_1_v_1_question_2.question_id
)

test_1_v_1_question_2_variant_2 = ormQuestionVariant(
    # answer_variant_id=5,
    answer_variant_text='Olya',
    question_id=test_1_v_1_question_2.question_id,
    answer_check=True
)

category_1 = ormTag(
    tag_category ='lol',
    count_of_likes=40
)

category_2 = ormTag(
    tag_category ='olol',
    count_of_likes=20

)

category_3 = ormTag(
    tag_category ='plol',
    count_of_likes=30
)

category_4 = ormTag(
    tag_category ='klol',
    count_of_likes=10

)

session.add_all([
    category_1, category_2, category_3, category_4
])
session.commit()

session.add_all([
    test_1_v_1_question_1_variant_1, test_1_v_1_question_1_variant_2, test_1_v_1_question_1_variant_3,
    test_1_v_1_question_2_variant_1, test_1_v_1_question_2_variant_2,
    category_1, category_2, category_3, category_4
])

session.commit()

