from app import app, mydb
from flask import render_template, redirect, request
from forms.tripform import TripForm
from bson.objectid import ObjectId

@app.route("/")
def homepage():
    # routes to the homepage and list of campgrounds
    try:
        triplist = mydb.trips.find({})
        trips = []
        for trip in triplist: 
            campgroundid = mydb.campgrounds.find_one({"_id":ObjectId(trip["campground"])})
            trip['campgroundname'] = campgroundid["name"]
            trip['parkname'] = campgroundid["parkname"]
            trips.append(trip)
        return render_template('home.html', trips=trips)
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
        campground = mydb.campgrounds.find_one({"_id":ObjectId(trip["campground"])})
        return render_template('trip.html', trip=trip, campground=campground)
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
        mycollection = mydb["trips"]
        mongoimport = { "tripname": tripname, "startdate": startdate, "enddate": enddate, "campground":campground }
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
        mycollection = mydb["trips"]
        mongoimport = {"$set": {"tripname": tripname, "startdate": startdate, "enddate": enddate, "campground":campground }}
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