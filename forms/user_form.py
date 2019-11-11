from flask_wtf import Form
from wtforms import StringField,SubmitField,  PasswordField, DateField, HiddenField,IntegerField
from wtforms import validators


class StudentForm(Form):
    student_id = StringField("student id: ",[
                                    validators.DataRequired("Please enter student id"),
                                    validators.Length(1, 20, "Student id should be from 1 to 20 symbols")
                                 ])

    student_name = StringField("student_name: ",[
                                    validators.DataRequired("Please enter student_name."),
                                    validators.Length(1, 20, "student_name should be from 1 to 20 symbols")
                                 ])

    student_surname = StringField("student_surname: ", [
                                    validators.DataRequired("Please enter student_surname."),
                                    validators.Length(1, 20, "student_surname should be from 1 to 20 symbols")
                                ])

    student_group = StringField("student_group: ", [
                                    validators.DataRequired("Please enter student_group."),

                                ])

    submit = SubmitField("Save")


class StudentForm1(Form):
    student_name = StringField("student_name: ", [
        validators.DataRequired("Please enter student_name."),
        validators.Length(1, 20, "student_name should be from 1 to 20 symbols")
    ])

    student_surname = StringField("student_surname: ", [
        validators.DataRequired("Please enter student_surname."),
        validators.Length(1, 20, "student_surname should be from 1 to 20 symbols")
    ])

    student_group = StringField("student_group: ", [
        validators.DataRequired("Please enter student_group."),

    ])

    submit = SubmitField("Save")


class PostForm(Form):
    post_id = IntegerField("post_id: ",[
                                    validators.DataRequired("Please enter post_id."),

                                 ])

    post_type = StringField("post_type: ",[
                                    validators.DataRequired("Please enter post_type."),
                                    validators.Length(1, 10, "post_type should be from 1 to 20 symbols")
                                 ])

    post_text = StringField("post_text: ",[
                                 validators.DataRequired("Please enter post_text"),
                                 validators.Length(3, 100, "post_text should be from 3 to 100 symbols")])
    stud_id = StringField("student id: ", [
        validators.DataRequired("Please enter student id"),

    ])

    disc_id = IntegerField("disc_id: ", [
        validators.DataRequired("Please enter disc_id"),

    ])
    name = StringField("name: ", [
        validators.DataRequired("Please enter name.")

    ])

    submit = SubmitField("Save")


class PostForm1(Form):

    post_type = StringField("post_type: ",[
                                    validators.DataRequired("Please enter post_type."),
                                    validators.Length(3, 10, "Name should be from 3 to 20 symbols")
                                 ])

    post_text = StringField("post_text: ",[
                                 validators.DataRequired("Please enter post_text"),
                                 validators.Length(3, 100, "post_text should be from 3 to 100 symbols")])
    stud_id = StringField("student id: ", [
        validators.DataRequired("Please enter student id"),

    ])
    disc_id = IntegerField("disc_id: ", [
        validators.DataRequired("Please enter disc_id"),

    ])

    name = StringField("name: ", [
        validators.DataRequired("Please enter name.")

    ])



    submit = SubmitField("Save")

class DisciplineForm(Form):
    disc_id = IntegerField("disc_id: ",[
                                    validators.DataRequired("Please enter disc_id."),

                                 ])


    disc_type = StringField("disc_type: ",[
                                    validators.DataRequired("Please enter disc_type.")
                                 ])



    disc_name = StringField("disc_name: ",[
                                 validators.DataRequired("Please enter disc_name.")
                                           ])

    submit = SubmitField("Save")


class DisciplineForm1(Form):
    disc_type = StringField("disc_type: ", [
        validators.DataRequired("Please enter disc_type.")
    ])

    disc_name = StringField("disc_name: ", [
        validators.DataRequired("Please enter disc_name.")
    ])

    submit = SubmitField("Save")



class CategoryForm1(Form):
    age_group = StringField("age_group: ", [
        validators.DataRequired("Please enter age_group.")
        #validators.('18+', 'junior')
    ])

    tags = StringField("tags: ", [
        validators.DataRequired("Please enter tags."),
        validators.Length(1, 10, "tags should be from 1 to 10 symbols")
    ])

    count_of_subscribers = IntegerField("count_of_subscribers: ", [
        validators.DataRequired("Please enter count_of_subscribers."),
        validators.Length(0, 1000, "count_of_subscribers should be from 0 to 1000 symbols")
    ])


    submit = SubmitField("Save")

