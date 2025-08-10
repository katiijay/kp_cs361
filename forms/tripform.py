from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from bson.objectid import ObjectId
from app import mydb

# gets a list of campgrounds to populate the results. 
campgrounds = mydb.campgrounds.find({})
campground_list = []
for doc in campgrounds:
    campground_name = doc['data']['name']
    campground_id = doc['_id']
    parkcode = doc['data']['parkCode']
    parkname = doc['parkName']
    campground_list.append((campground_id, str(parkname)+' Natl. Park - '+str(campground_name)))
# sorts campgrounds by park/campground
campground_list = sorted(campground_list, key=lambda x: x[1])

class TripForm(FlaskForm):

    tripname = StringField('Trip Name', validators=[DataRequired()])
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End Date')
    campground = SelectField('Campground Name', choices=campground_list, validators=[DataRequired()])
    submit = SubmitField('')