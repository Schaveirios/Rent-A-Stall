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
<<<<<<< HEAD
		sname = request.form['surname']
		fname = request.form['firstname']
		mname = request.form['middlename']
		paddress = request.form['presentaddress']
		contactnum = request.form['contactnumber']
		photo = request.form['photo']
		stallno = request.form['Stall Number']
		branchloc = request.form['Branch Location']
		if stallno in branchloc:
			if stallno == True:
				print "Occupied"
			else:
				models.addTenant()
		tenant = Tenant()

		msg = "Record sucessfully added."

		return return_template("resultadded.html", msg=msg)
=======
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

>>>>>>> 86f6410ac9b75feaa7c14f8f8ff2cedee61624df

@app.route("/stall")
def tenants():
	return render_templete("stalls.html")

@app.route("/AddStalls", methods = ["POST", "GET" ])
def AddStalls():
	if request.method == "POST"
		stallno = request.form['stallnumber']
		stallloc = request.form['stalllocation']
		rate = request.form['rate']
<<<<<<< HEAD

=======
                
>>>>>>> 86f6410ac9b75feaa7c14f8f8ff2cedee61624df
		stall = Stall()

		msg = "Record sucessfully added."

		return render_template("stalladded.html", msg=msg)



	


if __ == "__main__":
<<<<<<< HEAD
	app.run()
=======
	app.run()


def register():
    form = RegistrationForms(request.form)
    
>>>>>>> 86f6410ac9b75feaa7c14f8f8ff2cedee61624df
