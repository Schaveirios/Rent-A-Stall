import models
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from forms import addtenants, addstalls, addbranch, LogIn,RegisterForm
from sqlalchemy import and_
# import dt from 'datatables.net';
# import 'datatables.net-dt/css/jquery.datatables.css';
# from sqlalchemy import func     
# from datatables import datacolumns
# from werkzeug import secure_filename
#from flask_login import current_user, login_required
from app import dbase, app
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from models import Types, Branch, Stalls, Tenants, Users, Logs, Pays, Anonymous
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import required_roles


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/dashboard", methods=["GET"])
@app.route("/dashboard/", methods=["GET"])
@login_required
@required_roles(2)
def index():
    return render_template("dashboard.html")


@app.route("/admin_dashboard", methods=["GET"])
@app.route("/admin_dashboard/", methods=["GET"])
@login_required
@required_roles(1)
def index2():
    return render_template("admin_dashboard.html")    


@app.route("/successadd1", methods=["POST", "GET"])
@app.route("/successadd1/", methods=["POST", "GET"])
@login_required
@required_roles(1,2)
def added():
    return render_template("successadd1.html")



@app.route("/AddTenants", methods=["POST", "GET"])
@app.route("/AddTenants/", methods=["POST", "GET"])
@login_required
@required_roles(1, 2)
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

            branchLoc = form.branch.data
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()
            if stallnum:

                if stallnum.stall_status == "1":
                    flash("stall already Occupied")
                else:
                    loc = Branch.query.filter_by(branchID=branchLoc).first()
                    print
                    stall = Stalls.query.filter(
                        and_(Stalls.stall_no == stallno1, Stalls.branchID == loc.branchID)).first()
                    stall.stall_status = "1"
                    dbase.session.add(stall)
                    dbase.session.commit()
                    tenantForm = Tenants(contact_no=Contnum,
                                         first_name=firstname,
                                         mid_name=middlename,
                                         last_name=lastname,
                                         present_addr=Address,
                                         tenant_photo=TenantphotoID,
                                         stallID=stall.stallID
                                         )
                    dbase.session.add(tenantForm)
                    dbase.session.commit()
                    return render_template("successadd1.html")
            else:
                flash("stall already Occupied")
    return render_template("addtenant.html", form1=form)


@app.route("/AddTenants2", methods=["POST", "GET"])
@app.route("/AddTenants2/", methods=["POST", "GET"])
@login_required
@required_roles(1, 2)
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

            branchLoc = form.branch.data
            loc1 = Branch.query.filter_by(branchID=branchLoc).first()
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()

            if stallnum and loc1:

                if stallnum.stall_status == "1":
                    flash("stall already Occupied")
                else:
                    loc = Branch.query.filter_by(branchID=branchLoc).first()
                    stall = Stalls.query.filter(
                        and_(Stalls.stall_no == stallno1, Stalls.branchID == loc.branchID)).first()
                    if stall:
                        stall.stall_status = "1"
                        dbase.session.add(stall)
                        dbase.session.commit()
                        tenantForm = Tenants(contact_no=Contnum,
                                             first_name=firstname,
                                             mid_name=middlename,
                                             last_name=lastname,
                                             present_addr=Address,
                                             tenant_photo=TenantphotoID,
                                             stallID=stall.stallID
                                             )
                        dbase.session.add(tenantForm)
                        dbase.session.commit()
                        return render_template("successadd.html")
                    else:
                        flash('Stall is not available in the given branch')
            else:
                flash("Stall not found")
    return render_template("clerk_addtenant.html", form1=form)


@app.route("/AddStalls", methods=["POST", "GET"])
@app.route("/AddStalls/", methods=["POST", "GET"])
@login_required
@required_roles(1)
def AddStalls():
    form = addstalls()
    availstalls = Stalls.query.filter_by(stall_status= '0')
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
            flash('Stall already existing')
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
            return render_template("successadd1.html")
    return render_template("addstall.html", form=form, availstalls = availstalls)



@app.route("/clerk", methods = ["POST", "GET" ])
@app.route("/clerk/", methods = ["POST", "GET" ])
@login_required
@required_roles(1)
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
        regclerk = Users.query.filter_by(username=form.username.data).first()
        if regclerk:
            flash('username is already used')
        else:
            dbase.session.add(uForm)
            dbase.session.commit()
            return render_template('successadd1.html')
    return render_template("addclerk.html", form=form)

@app.route('/', methods=["GET", "POST"])
@app.route('//', methods=["GET","POST"])
def login():
    form = LogIn()
    Branch.branch_types()
    Types.stall_types()
    print current_user
    if current_user.is_active():
        if current_user.roleID == '1':
            return redirect(url_for('index2'))
        else:
            return redirect(url_for('index'))
    else:
        if request.method == "POST" and form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            print user.username
            if user:
                if user.roleID == 2:
                    if user is not None and check_password_hash(user.passwrd, form.passwrd.data):
                        login_user(user)
                        return redirect(url_for('index'))
                    return '<h1>Invalid username or password!!!!!</h1>'
                elif user.roleID == 1:
                    if user is not None and check_password_hash(user.passwrd, form.passwrd.data):
                        login_user(user)
                        return redirect(url_for('index2'))
                    return '<h1>Invalid username or password!!!!!</h1>'

                else:
                    return '<h1>Invalid username or password!!!!!</h1>'
            else:
                return '<h1>Invalid username or password!!!!!</h1>'
    return render_template('login.html', form= form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('login'))


def pageFormula(total, perpage):
    if total % perpage == 0:
        return total / perpage
    return (total / perpage) + 1

@app.route('/showtenants', methods=["GET", "POST"])
@app.route('/showtenants/', methods=["GET", "POST"])
def tenantslist():
  x = []
  result = Tenants.query.order_by(Tenants.first_name).paginate(1,10,True)
  for r in result.items:
      stall = Stalls.query.filter_by(stallID=r.stallID).first()
      x.append(stall.stall_no)
  #x = len(Tenants.query.order_by(Tenants.first_name).all())
  return render_template('showtenants.html',result=result, x=x)# , stry=pageFormula(x, 11))
  # return jsonify({'firstname':firstname, 'middlename':middlename, 'lastname':lastname})

@app.route('/showstalls', methods=["GET", "POST"])
@app.route('/showstalls/', methods=["GET", "POST"])
def stalllist():
	x = []
	result = Stalls.query.order_by(Stalls.stall_no).paginate(1,8,True)
	for r in result.items:
		tayp = Types.query.filter_by(typeID =r.typeID).first()
		x.append(tayp.stall_type)
	return render_template('showstalls.html', result=result, x=x)  