#import models
from flask import Flask, render_template, request, redirect, url_for
from forms import addtenants, addstalls, addbranch, RegisterForm, LogIn
from sqlalchemy import and_
# from werkzeug import secure_filename
#from flask_login import current_user, login_required
from app import dbase, app
from models import Types, Branch, Stalls, Tenants, Users, Logs, Pays
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/", methods=["GET"])
@app.route("//", methods=["GET"])
def index():
    return render_template("dashboard.html")


@app.route("/admin_dashboard", methods=["GET"])
@app.route("/admin_dashboard/", methods=["GET"])
def index2():
    Branch.branch_types()
    Types.stall_types()
    return render_template("admin_dashboard.html")    


@app.route("/successadd", methods=["POST", "GET"])
@app.route("/successadd/", methods=["POST", "GET"])
#@login_required
def added():
    return render_template("successadd.html")


@app.route("/AddTenants", methods=["POST", "GET"])
@app.route("/AddTenants/", methods=["POST", "GET"])
def AddTenants():
    form = addtenants()
    if request.method == "POST":
        if form.validate_on_submit():

            firstname = form.fname.data
            middlename = form.mname.data
            lastname = form.lname.data
            Address = form.address.data
            Contnum = form.contnum.data
            TenantphotoID = form.tenantphotoID.data
            stallno1 = form.stallno.data

            stallType = form.stalltype.data
            type = Types.query.filter_by(stall_type=stallType).first()

            if type:
                t = type.typeID

            else:
                Stalltype = Types(stall_type=stallType)

                dbase.session.add(Stalltype)
                dbase.session.commit()

            branchLoc = form.stallloc.data
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()
            if stallnum:
                
                if stallnum.stall_status == "1":
                    return "<h3>Stall is Already Occupied</h3>"
                else:
                    loc = Branch.query.filter_by(branch_loc=branchLoc).first()
                    stall = Stalls.query.filter(and_(Stalls.stall_no == stallno1, Stalls.branchID == loc.branchID)).first()
                    stall.stall_status = "1"
                    dbase.session.add(stall)
                    dbase.session.commit()
                    tenantForm = Tenants(contact_no=Contnum ,
                                        first_name=firstname ,
                                        mid_name=middlename ,
                                        last_name=lastname ,
                                        present_addr=Address ,
                                        tenant_photo=TenantphotoID ,
                                        stallID=stall.stallID
                                        )
                    dbase.session.add(tenantForm)
                    dbase.session.commit()
                    return render_template("successadd.html")
            else:
                return "<h3>Stall not found</h3>"
    return render_template("addtenant.html", form1=form)

@app.route("/AddTenants2", methods=["POST", "GET"])
@app.route("/AddTenants2/", methods=["POST", "GET"])
def AddTenants2():
    form = addtenants()
    if request.method == "POST":
        if form.validate_on_submit():

            firstname = form.fname.data
            middlename = form.mname.data
            lastname = form.lname.data
            Address = form.address.data
            Contnum = form.contnum.data
            TenantphotoID = form.tenantphotoID.data
            stallno1 = form.stallno.data

            stallType = form.stalltype.data
            type = Types.query.filter_by(stall_type=stallType).first()

            if type:
                t = type.typeID

            else:
                Stalltype = Types(stall_type=stallType)

                dbase.session.add(Stalltype)
                dbase.session.commit()

            branchLoc = form.stallloc.data
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()
            if stallnum:
                
                if stallnum.stall_status == "1":
                    return "<h3>Stall is Already Occupied</h3>"
                else:
                    loc = Branch.query.filter_by(branch_loc=branchLoc).first()
                    stall = Stalls.query.filter(and_(Stalls.stall_no == stallno1, Stalls.branchID == loc.branchID)).first()
                    stall.stall_status = "1"
                    dbase.session.add(stall)
                    dbase.session.commit()
                    tenantForm = Tenants(contact_no=Contnum ,
                                        first_name=firstname ,
                                        mid_name=middlename ,
                                        last_name=lastname ,
                                        present_addr=Address ,
                                        tenant_photo=TenantphotoID ,
                                        stallID=stall.stallID
                                        )
                    dbase.session.add(tenantForm)
                    dbase.session.commit()
                    return render_template("successadd.html")
            else:
                return "<h3>Stall not found</h3>"
    return render_template("clerk_addtenant.html", form1=form)    


@app.route("/AddStalls", methods=["POST", "GET"])
@app.route("/AddStalls/", methods=["POST", "GET"])
# @login_required
def AddStalls():
    form = addstalls()
    if request.method == "POST":
        stallNo = form.stallno.data
        stallLoc = form.stallloc.data
        Rate = form.rate.data
        BranchLoc = form.Branchloc.data
        loc = Branch.query.filter_by(branch_loc=BranchLoc).first()
        locid = loc.branchID
        stalltype = form.stalltype.data
        type = Types.query.filter_by(stall_type=stalltype).first()
        if type:
            t = type.typeID
        else:
            Stalltype = Types(stall_type=stalltype)

            dbase.session.add(Stalltype)
            dbase.session.commit()

            type1 = Types.query.filter_by(stall_type=stalltype).first()
            t = type1.typeID

        stallstat = Stalls.query.filter_by(stall_no=stallNo).first()
        if stallstat:
            return "<h3>Stall is already existing</h3>"
        else:
            stallform = Stalls(stall_rate=Rate,
                            stall_loc=stallLoc,
                            stall_status="0",
                            stall_no=stallNo,
                            branchID=locid,
                            typeID=t
                            )
            dbase.session.add(stallform)
            dbase.session.commit()
            return render_template("successadd.html")
    return render_template("addstall.html", form=form)



@app.route("/clerk", methods = ["POST", "GET" ])
@app.route("/clerk/", methods = ["POST", "GET" ])
# @login_required
def AddClerk():
    form = RegisterForm()
    if request.method=='POST' and form.validate_on_submit():
        uForm = Users(username=form.username.data,
                         passwrd=form.password.data,
                         first_name=form.fname.data,
                         mid_name=form.mname.data ,
                         last_name = form.lname.data,
                         contact_no = form.ContNum.data,
                         branchID = form.branchID.data,
                         roleID = '2'
                         )
        dbase.session.add(uForm)
        dbase.session.commit()
        return render_template('successadd.html')
    return render_template("addclerk.html", form=form)

@app.route('/login', methods=["GET", "POST"])
@app.route('/login/', methods=["GET","POST"])
def login():
    form = LogIn()
    if request.method=='POST':
        print 'gdg'
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            print user.username
            if user is not None and check_password_hash(user.passwrd, form.passwrd.data):
                login(user)
                return redirect(url_for('index'))
            return '<h1>Invalid username or password!!!!!</h1>'
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


