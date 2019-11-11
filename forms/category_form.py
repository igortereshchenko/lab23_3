from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class CategoryForm(Form):

    name = StringField("Name: ", [  validators.DataRequired("Please enter your tags."),
                                   validators.Length(10, 1000, "Name should be from 10 to 100 symbols")])

    tags = StringField("Tags: ")


    count_of_subscribers = IntegerField("Count Subscribers : ", [
                               validators.DataRequired("Please enter your name."),
                               validators.NumberRange(0, 10000, "Name should be from 0 to 100 symbols")
                                                       ])

    comment = StringField("Comment: ")

    submit = SubmitField("Save")


