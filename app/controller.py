import models
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from forms import addtenants, addstalls, LogIn,RegisterForm, PaymentForm
from sqlalchemy import and_
from app import dbase, app
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from models import Types, Branch, Stalls, Tenants, Users, Logs, Pays, Anonymous
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import required_roles
from werkzeug import secure_filename
from PIL import Image
import datetime
import time
import os

now= datetime.datetime.now()
datelog = str(now)


img_folder = 'static/profile/'
available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension


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
    availstalls = Stalls.query.filter_by(stall_status= '0')
    if request.method == "POST":
        if form.validate_on_submit():
            print "naaaaaa diiriiii"

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

            # branchLoc = form.branch.data
            # loc1 = Branch.query.filter_by(branchID=branchLoc).first()
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()

            if stallnum:
                if stallnum.stall_status == "1":
                    flash("stall already Occupied")
                else:
                    # loc = Branch.query.filter_by(branchID=branchLoc).first()
                    stall = Stalls.query.filter_by(stall_no=stallno1).first()
                    if stall:                        
                        tenantForm = Tenants(contact_no=Contnum,
                                             first_name=firstname,
                                             mid_name=middlename,
                                             last_name=lastname,
                                             present_addr=Address,
                                             # tenant_photo=TenantphotoID,
                                             stallID=stall.stallID
                                             )
                        if form.tenantphotoID.data:
                            stall.stall_status = "1"
                            dbase.session.add(stall)
                            dbase.session.commit()
                            dbase.session.add(tenantForm)
                            dbase.session.commit()
                        else:
                            return render_template("addtenant.html", form1=form, availstalls = availstalls)

                        profile_entry = ""
                        te = Tenants.query.all()
                        TenantphotoID = img_folder + str(len(te))
                        if os.path.isdir(TenantphotoID) == False:
                            os.makedirs(TenantphotoID)

                        print form.tenantphotoID.data.filename 
                        if form.tenantphotoID.data.filename == None or form.tenantphotoID.data.filename == "":
                            tenants.tenant_photo = tenants.tenant_photo
                        else:
                            if form.tenantphotoID.data and allowed_file(form.tenantphotoID.data.filename):
                                filename = secure_filename(form.tenantphotoID.data.filename)
                                form.tenantphotoID.data.save(os.path.join(TenantphotoID + '/', filename))

                                uploadFolder = TenantphotoID + '/'
                                nameNew = str(int(time.time())) + '.' + str(os.path.splitext(filename)[1][1:])
                                os.rename(uploadFolder + filename, uploadFolder + nameNew)
                                profile_entry = uploadFolder+nameNew

                                t = Tenants.query.filter_by(tenantID=len(te)).first()
                                t.tenant_photo = profile_entry
                                print profile_entry
                                dbase.session.add(t)
                                user = current_user
                                lgdate= str(now)
                                msg = user.username + " added a tenant "
                                logmessage = Logs(details = msg,
                                                    log_date = lgdate)
                                dbase.session.add(logmessage)
                                dbase.session.commit()
                        return render_template("successadd1.html")
                    else:
                        flash('Stall is not available in the given branch')
            else:
                flash("Stall not found")
    return render_template("addtenant.html", form1=form, availstalls = availstalls)


@app.route("/AddTenants2", methods=["POST", "GET"])
@app.route("/AddTenants2/", methods=["POST", "GET"])
@login_required
@required_roles(1, 2)
def AddTenants2():
    form = addtenants()
    availstalls = Stalls.query.filter_by(stall_status= '0')
    if request.method == "POST":
        if form.validate_on_submit():
            print "naaaaaa diiriiii"

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

            # branchLoc = form.branch.data
            # loc1 = Branch.query.filter_by(branchID=branchLoc).first()
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()

            if stallnum:
                if stallnum.stall_status == "1":
                    flash("stall already Occupied")
                else:
                    # loc = Branch.query.filter_by(branchID=branchLoc).first()
                    stall = Stalls.query.filter_by(stall_no=stallno1).first()
                    if stall:                        
                        tenantForm = Tenants(contact_no=Contnum,
                                             first_name=firstname,
                                             mid_name=middlename,
                                             last_name=lastname,
                                             present_addr=Address,
                                             # tenant_photo=TenantphotoID,
                                             stallID=stall.stallID
                                             )
                        if form.tenantphotoID.data:
                            stall.stall_status = "1"
                            dbase.session.add(stall)
                            dbase.session.commit()
                            dbase.session.add(tenantForm)
                            dbase.session.commit()
                        else:
                            return render_template("clerk_addtenant.html", form1=form, availstalls = availstalls)

                        profile_entry = ""
                        te = Tenants.query.all()
                        TenantphotoID = img_folder + str(len(te))
                        if os.path.isdir(TenantphotoID) == False:
                            os.makedirs(TenantphotoID)

                        print form.tenantphotoID.data.filename 
                        if form.tenantphotoID.data.filename == None or form.tenantphotoID.data.filename == "":
                            tenants.tenant_photo = tenants.tenant_photo
                        else:
                            if form.tenantphotoID.data and allowed_file(form.tenantphotoID.data.filename):
                                filename = secure_filename(form.tenantphotoID.data.filename)
                                form.tenantphotoID.data.save(os.path.join(TenantphotoID + '/', filename))

                                uploadFolder = TenantphotoID + '/'
                                nameNew = str(int(time.time())) + '.' + str(os.path.splitext(filename)[1][1:])
                                os.rename(uploadFolder + filename, uploadFolder + nameNew)
                                profile_entry = uploadFolder+nameNew

                                t = Tenants.query.filter_by(tenantID=len(te)).first()
                                t.tenant_photo = profile_entry
                                print profile_entry
                                dbase.session.add(t)
                                user = current_user
                                lgdate= str(now)
                                msg = user.username + " added a tenant "
                                logmessage = Logs(details = msg,
                                                    log_date = lgdate)
                                dbase.session.add(logmessage)
                                dbase.session.commit()
                        return render_template("successadd.html")
                    else:
                        flash('Stall is not available in the given branch')
            else:
                flash("Stall not found")
    return render_template("clerk_addtenant.html", form1=form, availstalls = availstalls)

@app.route("/AddStalls", methods=["POST", "GET"])
@app.route("/AddStalls/", methods=["POST", "GET"])
@login_required
@required_roles(1)
def AddStalls():
    form = addstalls()
    if request.method == "POST":
        if form.validate_on_submit():
            stallNo = form.stallno.data
            stallLoc = form.stallloc.data
            Rate = form.rate.data
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
                stallform = Stalls(stall_rate=int(Rate),
                                stall_loc=stallLoc,
                                stall_status="0",
                                stall_no=int(stallNo),
                                typeID=t
                                )
                dbase.session.add(stallform)
                user = current_user
                lgdate= str(now)
                msg = user.username + " added a tenant "
                logmessage = Logs(details = msg,
                                        log_date = lgdate)
                dbase.session.add(logmessage)
                dbase.session.commit()
                return render_template("successadd1.html")
    return render_template("addstall.html", form=form)



@app.route("/clerk", methods = ["POST", "GET" ])
@app.route("/clerk/", methods = ["POST", "GET" ])
@login_required
@required_roles(1)
def AddClerk():
    form = RegisterForm()
    if request.method=='POST':
        if form.validate_on_submit():
            print "akdnfjafjljlas"
            uForm = Users(username=form.username.data,
                            passwrd=form.password.data,
                            first_name=form.fname.data,
                            mid_name=form.mname.data ,
                            last_name = form.lname.data,
                            contact_no = form.ContNum.data,
                            # branchID = "1",
                            roleID = '2'
                            )
            regclerk = Users.query.filter_by(username=form.username.data).first()
            if regclerk:
                flash('username is already used')
            else:
                print "sjsjdjdjjdjdjdjd"
                dbase.session.add(uForm)
                user = current_user
                lgdate= str(now)
                msg = user.username + " added a clerk "
                logmessage = Logs(details = msg,
                                    log_date = lgdate)
                dbase.session.add(logmessage)
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
        if current_user.roleID == 1:
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
                        msg = user.username + " logs in"
                        lgdate = str(now)
                        print lgdate
                        logmessage = Logs(details = msg,
                                          log_date = lgdate)
                        dbase.session.add(logmessage)
                        login_user(user)
                        return redirect(url_for('index'))
                    return '<h1>Invalid username or password!</h1>'
                elif user.roleID == 1:
                    if user is not None and check_password_hash(user.passwrd, form.passwrd.data):
                        msg = user.username + " logs in"
                        lgdate = str(now)
                        print lgdate
                        logmessage = Logs(details = msg,
                                          log_date = lgdate)
                        dbase.session.add(logmessage)
                        login_user(user)
                        login_user(user)
                        return redirect(url_for('index2'))
                    return '<h1>Invalid username or password!</h1>'

                else:
                    return '<h1>Invalid username or password!</h1>'
            else:
                return '<h1>Invalid username or password!</h1>'
    return render_template('login.html', form=form)


@app.route('/logout')
@app.route('/logout/')
@login_required
def logout():
    user = current_user
    lgdate = str(now)
    msg = user.username + " logs out "
    logmessage = Logs(details=msg,
                      log_date=lgdate)
    dbase.session.add(logmessage)
    dbase.session.commit()
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('login'))

def pageFormula(total, perpage):
    if total % perpage == 0:
        return total / perpage
    return (total / perpage) + 1

@app.route('/showtenants', methods=["GET", "POST"])
@app.route('/showtenants/', methods=["GET", "POST"])
@login_required
@required_roles(1,2)
def tenantslist():
    user = current_user
    lgdate = str(now)
    msg = user.username + " viewed the tenant list "
    logmessage = Logs(details=msg,
                      log_date=lgdate)
    dbase.session.add(logmessage)
    dbase.session.commit()
    x = []  
    result = Tenants.query.order_by(Tenants.first_name).all()#.paginate(1,2,True)
    for r in result:        
      stall = Stalls.query.filter_by(stallID=r.stallID).first()
      x.append(stall.stall_no)

    #x = len(Tenants.query.order_by(Tenants.first_name).all())
    return render_template('showtenants.html',result=result, x=x)# , stry=pageFormula(x, 11))
    # return jsonify({'firstname':firstname, 'middlename':middlename, 'lastname':lastname})

@app.route('/showstalls', methods=["GET", "POST"])
@app.route('/showstalls/', methods=["GET", "POST"])
@login_required
@required_roles(1,2)
def stalllist():
    user = current_user
    lgdate = str(now)
    print lgdate
    msg = user.username + " viewed the stalls "
    logmessage = Logs(details=msg,
                      log_date=lgdate)
    dbase.session.add(logmessage)
    dbase.session.commit()
    x = []
    result = Stalls.query.order_by(Stalls.stall_no).all()#.paginate(1,11,True)
    for r in result:
        tayp = Types.query.filter_by(typeID =r.typeID).first()
        x.append(tayp.stall_type)
    return render_template('showstalls.html', result=result, x=x)


@app.route('/logs', methods=["GET", "POST"])
@app.route('/logs/', methods=["GET", "POST"])
@login_required
@required_roles(1)
def logs():
    print datelog   
    user = current_user
    lgdate = datelog
    msg = user.username + " viewed the logs "
    logmessage = Logs(details=msg,
                      log_date=lgdate)
    dbase.session.add(logmessage)
    dbase.session.commit()
    showlogs = Logs.query.all()
    return render_template('logs.html', showlogs=showlogs)

@app.route('/payment/<int:id>/<int:s_id>/', methods=["GET", "POST"])
@login_required
@required_roles(1,2)
def payment(id, s_id):
    someNum = Stalls.query.filter_by(stallID=s_id).first()
    typee = Types.query.filter_by(typeID=someNum.typeID).first()
    tenant_1 = Tenants.query.filter(and_(Tenants.tenantID==id, Tenants.stallID==someNum.stallID)).first()

    form = PaymentForm()
    if request.method=='POST' and form.validate_on_submit():
        uForms = Pays(month=form.month.data,
                        amount=form.amount.data,
                         sCharge=form.sCharge.data,
                         total=form.total.data ,
                         or_no=form.or_no.data,
                         date_issued=form.date_issued.data,
                         issued_by=form.issued_by.data,
                        tenantID = tenant_1.tenantID,
                        stallID = someNum.stallID
                       )

        dbase.session.add(uForms)
        dbase.session.commit()
        return redirect(url_for("paymenttable", id=id, s_id=s_id))
    if current_user.roleID == 1:
        return render_template("payment_admin.html", form=form, tenant=tenant_1, stall=someNum, typee=typee)
    return render_template("payment.html", form=form, tenant=tenant_1, stall=someNum, typee=typee)


@app.route('/payment_table/<int:id>/<int:s_id>/', methods = ["GET", "POST"])
@login_required
@required_roles(1,2)
def paymenttable(id, s_id):
    pays = Pays.query.filter(and_(Pays.tenantID==id, Pays.stallID==s_id)).all()
    someNum = Stalls.query.filter_by(stallID=s_id).first()
    tenant_1 = Tenants.query.filter(and_(Tenants.tenantID==id, Tenants.stallID==someNum.stallID)).first()
    typee = Types.query.filter_by(typeID=someNum.typeID).first()

    if current_user.roleID == 1:
        return render_template('paymenttable_admin.html', pays=pays, id=id, s_id=s_id, stall=someNum, typee=typee, tenant=tenant_1)
    return render_template('paymenttable.html', pays=pays, id=id, s_id=s_id, stall=someNum, typee=typee, tenant=tenant_1)

