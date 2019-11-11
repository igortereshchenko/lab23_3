from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class PostForm(Form):

   post_id = IntegerField("Id: ",[
                                    validators.DataRequired("Please enter your id."),
                                    validators.NumberRange(0, 10000, "Name should be from 3 to 20 symbols")
                                 ])



   submit = SubmitField("Save")


