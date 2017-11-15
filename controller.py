import models
from flask import flask, render_template, request
from forms import Tenants, Stalls

app = Flask(__name__)

@app.route("/tenants")
def tenants():
	return render_templete("tenants.html")

@app.route("/AddTenants", methods = ["POST", "GET" ])
def AddTenants():
	if request.method == "POST"
		if form.validate_on_submit():

			user.first_name = form.first_name.data
			user.middle_name = form.middle_name.data
        	user.last_name = form.last_name.data
			paddress = request.form['presentaddress']
			contactnum = request.form['contactnumber']
			photo = request.form['photo']
			stallno = request.form['Stall Number']
        	branchloc = request.form['Branch Location']
        	
			dbase.tenants.add()
    		dbase.tenants.commit()
    	else:


@app.route("/stall")
def tenants():
	return render_templete("stalls.html")

@app.route("/AddStalls", methods = ["POST", "GET" ])
def AddStalls():
	if request.method == "POST"
		stallno = request.form['stallnumber']
		stallloc = request.form['stalllocation']
		rate = request.form['rate']
                
		stall = Stall()

		msg = "Record sucessfully added."

		return render_template("stalladded.html", msg=msg)



	


if __ == "__main__":
	app.run()


def register():
    form = RegistrationForms(request.form)
    