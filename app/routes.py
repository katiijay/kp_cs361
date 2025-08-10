from app import app, mydb
from flask import render_template, redirect, request
from forms.tripform import TripForm
from forms.notesform import NotesForm
from bson.objectid import ObjectId
from flask_caching import Cache
import requests
import json

cache = Cache(app)
@cache.cached(timeout=300)
# set caching for 5 minutes due to several API calls. 

@app.route("/")
def homepage():
    # routes to the homepage and list of campgrounds
    try:
        triplist = mydb.trips.find({})
        return render_template('home.html', trips=triplist)
    except Exception: 
        msg = 'trip table broken'
        return msg
    
@app.route("/help")
def helppage():
    # routes to the helppage
    return render_template('help.html')

@app.route("/trip/<tripnumber>")
def trip(tripnumber):
    # routes to the "view details" page for a given trip
    if mydb.trips.find({"_id":tripnumber}) is not None:
        trip = mydb.trips.find_one({"_id":ObjectId(tripnumber)})
        
        # Gets Notes form and notes values if it exists. 
        form = NotesForm(trip="tripnumber")
        notes = requests.get(url=f'http://127.0.0.1:5001/{tripnumber}')
        notes = notes.json()

        
        # gets alerts and activities
        parkcode = trip['parkCode']
        alerts = requests.get(url='http://127.0.0.1:5003/alerts', params={'parkcode':parkcode})
        alerts = alerts.json()
        activities = requests.get(url='http://127.0.0.1:5004/activities', params={'parkcode':parkcode})
        activities = activities.json()

        # gets weather and return up to 5 days, but no more than 5 days of camping trip weather
        weather_list = []
        tripstart = trip['startdate']
        tripend = trip['enddate']
        startdate = int(tripstart.replace('-',''))
        enddate = int(tripend.replace('-',''))
        lat = trip['latitude']
        long = trip['longitude']
        
        maxcounter = 0
        for date in range(startdate, enddate+1):
            if maxcounter < 5:
                tripdate = str(date)
                weather = requests.get(url='http://127.0.0.1:5002/geoforecast', params={'lat':lat,'long':long, 'date':tripdate})
                weather = weather.json()
                weather['date'] = f'{tripdate[0:4]}-{tripdate[4:6]}-{tripdate[6:8]}'
                weather['weatherCodeName'] = (weather['weatherCodeName'].replace('-',' ')).capitalize()
                weather_list.append(weather)
                maxcounter += 1
            else:
                break

        return render_template('trip.html', trip=trip, alerts=alerts, activities=activities, weather=weather_list, form=form, notes=notes)
    else: 
        msg = 'Could not find that trip ID'
        return msg
    

@app.route("/trip/<tripnumber>/notes", methods=['GET', 'POST'])
def tripnotes(tripnumber):
    if mydb.trips.find({"_id":tripnumber}) is not None:
        trip = mydb.trips.find_one({"_id":ObjectId(tripnumber)})
        notes = requests.get(url=f'http://127.0.0.1:5001/{tripnumber}')
        notes = notes.json()

        form = NotesForm(trip="tripnumber")
        if form.validate_on_submit():

            url = f'http://127.0.0.1:5001/{tripnumber}'
            notes = request.form['notes']
            data = {'notes': notes}
            headers = {'Content-type':'application/json', 'Accept':'application/json'}
            requests.post(url=url, data=json.dumps(data), headers=headers)
            return redirect(f'/trip/{tripnumber}')
    
        return render_template('tripnotes.html', trip=trip, form=form, notes=notes)
    else: 
        msg = 'Could not find that trip ID'
        return msg


@app.route("/addnewtrip", methods=['GET', 'POST'])
def addnewpage():
    # routes to the add new trip page
    form = TripForm()
    if form.validate_on_submit():
        tripname = request.form['tripname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        campground = request.form['campground']
        campgrounddata = mydb.campgrounds.find_one({'_id':ObjectId(campground)})['data']
        campgroundname = campgrounddata['name']
        latitude = campgrounddata['latitude']
        longitude = campgrounddata['longitude']
        parkcode = campgrounddata['parkCode']
        parkdata = mydb.parks.find_one({'_id':parkcode})['data']
        parkname = parkdata['fullName']
        addressline1 = parkdata['addresses'][0]['line1']
        addresscity = parkdata['addresses'][0]['city']
        addressstate = parkdata['addresses'][0]['stateCode']
        addresscountry = parkdata['addresses'][0]['countryCode']
        addresszip = parkdata['addresses'][0]['postalCode']
        mycollection = mydb["trips"]
        mongoimport = {     "tripname": tripname, "startdate": startdate, "enddate": enddate, 
                       "campground":campground, 'campgroundName':campgroundname, 'latitude': latitude,
                       'longitude': longitude, 'parkCode': parkcode, 'parkName': parkname, 
                       'addressline1':addressline1, 'addresscity':addresscity, 'addressstate':addressstate,
                       'addresscountry':addresscountry, 'addresszip':addresszip
                       }
        mycollection.insert_one(mongoimport)
        return redirect('/')
    else:
        print(form.errors)
    return render_template('addnewtrip.html', form=form)


@app.route("/updatetrip/<tripnumber>", methods=['GET', 'POST'])
def updatetrippage(tripnumber):
    # routes to the update existing trip page
    trip = mydb.trips.find_one({"_id":ObjectId(tripnumber)})
    form = TripForm(campground=trip["campground"])
    if form.validate_on_submit():
        tripname = request.form['tripname']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        campground = request.form['campground']
        campgrounddata = mydb.campgrounds.find_one({'_id':ObjectId(campground)})['data']
        campgroundname = campgrounddata['name']
        latitude = campgrounddata['latitude']
        longitude = campgrounddata['longitude']
        parkcode = campgrounddata['parkCode']
        parkdata = mydb.parks.find_one({'_id':parkcode})['data']
        parkname = parkdata['fullName']
        addressline1 = parkdata['addresses'][0]['line1']
        addresscity = parkdata['addresses'][0]['city']
        addressstate = parkdata['addresses'][0]['stateCode']
        addresscountry = parkdata['addresses'][0]['countryCode']
        addresszip = parkdata['addresses'][0]['postalCode']
        mycollection = mydb["trips"]
        mongoimport = {"$set": { "tripname": tripname, "startdate": startdate, "enddate": enddate, 
                       "campground":campground, 'campgroundName':campgroundname, 'latitude': latitude,
                       'longitude': longitude, 'parkCode': parkcode, 'parkName': parkname, 
                       'addressline1':addressline1, 'addresscity':addresscity, 'addressstate':addressstate,
                       'addresscountry':addresscountry, 'addresszip':addresszip
                       }}
        mycollection.update_one(trip, mongoimport)
        return redirect('/')
    else:
        print(form.errors)
    return render_template('updatetrip.html', form=form, trip=trip)


@app.route("/delete/<tripnumber>")
def deletetrippage(tripnumber):
    # routes to delete a trip (immediately redirects home after)
    if mydb.trips.find({"_id":tripnumber}) is not None:
        trip = mydb.trips.find_one({"_id":ObjectId(tripnumber)})
        mycollection = mydb["trips"]
        mycollection.delete_one(trip)
        return redirect('/')
    else: 
        msg = 'Could not find that trip ID'
        return msg