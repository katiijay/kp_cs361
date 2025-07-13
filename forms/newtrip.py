from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

class NewTripForm(FlaskForm):
    tripname = StringField('Trip Name', validators=[DataRequired()])
    startdate = DateField('Start Date', validators=[DataRequired()])
    enddate = DateField('End Date', validators=[DataRequired()])
    campgroundname = StringField('Campground Name', validators=[DataRequired()])
    submit = SubmitField('Create Trip')