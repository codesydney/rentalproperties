from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    room_drop = [(-1,'Select'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8')]

    min_bedrooms = SelectField('Minimum Bedrooms', choices=room_drop, coerce=int)
    min_bathrooms = SelectField('Minimum Bathrooms', choices=room_drop, coerce=int)
    max_price = IntegerField('Maximum Rental Price per week*', validators=[InputRequired()])
    postcode = IntegerField('Postcode*', validators=[InputRequired()])
    #surround_suburbs = BooleanField('Search surrounding suburbs')
    submit = SubmitField('Submit')
