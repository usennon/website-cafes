from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, URL


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign me up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in!")


class AddCafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("Map url", validators=[DataRequired(), URL()])
    img_url = StringField("Img url", validators=[DataRequired()])
    location = StringField("Place location", validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    coffee_price = StringField('Coffee price')
    has_sockets = SelectField("Sokects in place", choices=[0, 1])
    has_toilet = SelectField("Is there a toilet", choices=[0, 1])
    can_take_calls = SelectField("Can take calls?", choices=[0, 1])
    has_wifi = SelectField("Wifi strength rating", choices=[0, 1])
    submit = SubmitField('Submit')


class CafeSuggestForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("Map url", validators=[DataRequired(), URL()])
    location = StringField("Place location", validators=[DataRequired()])
    cafe_site = StringField('Caffe site', validators=[URL()])
    submit = SubmitField('Submit')