from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class PostCategoryForm(Form):

   post_id = IntegerField("Post id: ", [
                                    validators.DataRequired("Please enter your id."),
                                    validators.NumberRange(0, 10000, "Name should be from 3 to 20 symbols")
                                 ])

   name = IntegerField("name: ", [
                                   validators.DataRequired("Please enter your id."),
                                   validators.NumberRange(0, 10000, "Name should be from 3 to 20 symbols")
                               ])


   submit = SubmitField("Save")


