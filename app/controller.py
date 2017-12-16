import models
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from forms import addtenants, addstalls, LogIn,RegisterForm, PaymentForm, edit_tenant_form
from sqlalchemy import and_
from app import dbase, app
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from models import Types, Branch, Stalls, Tenants, Users, Logs, Pays, Anonymous, Rents#
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import required_roles
from werkzeug import secure_filename
from PIL import Image
import datetime
import time
import os

now= datetime.datetime.now()
datelog = str(now)


img_folder = 'app/static/profile/'
loc_default = 'static/profile/default.jpg'
available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def search_panel(cond):
    if cond==1:
        y = []
        result2 = Stalls.query.order_by(Stalls.stall_no).all()#.paginate(1,11,True)
        for r in result2:
            type = Types.query.filter_by(typeID =r.typeID).first()
            y.append(type.stall_type)
        return result2, y

    x = []
    result = Tenants.query.order_by(Tenants.first_name).all()#.paginate(1,2,True)
    for r in result:
      stall = Stalls.query.filter_by(stallID=r.stallID).first()
      x.append(stall.stall_no)
    return result, x

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
    return render_template("dashboard.html", result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


@app.route("/admin_dashboard", methods=["GET"])
@app.route("/admin_dashboard/", methods=["GET"])
@login_required
@required_roles(1)
def index2():
    return render_template("admin_dashboard.html", result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


@app.route("/successadd1", methods=["POST", "GET"])
@app.route("/successadd1/", methods=["POST", "GET"])
@login_required
@required_roles(1,2)
def added():
    return render_template("successadd1.html", result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])

@app.route("/AddTenants", methods=["POST", "GET"])
@app.route("/AddTenants/", methods=["POST", "GET"])
@login_required
@required_roles(1, 2)
def AddTenants():
    form = addtenants()
    availstalls_y = []
    availstalls = Stalls.query.filter_by(stall_status= '0').all()#.paginate(1,11,True)
    for r in availstalls:
        type = Types.query.filter_by(typeID =r.typeID).first()
        availstalls_y.append(type.stall_type)

    x = []
    result = Tenants.query.order_by(Tenants.first_name).all()#.paginate(1,2,True)
    for r in result:
        stall = Stalls.query.filter_by(stallID=r.stallID).first()
        x.append(stall.stall_no)

    if request.method == "POST":
        print "scull"
        if form.validate_on_submit():
            print "hello1"
            firstname = form.fname.data
            middlename = form.mname.data
            lastname = form.lname.data
            Address = form.address.data
            Contnum = form.contnum.data
            TenantphotoID = form.tenantphotoID.data
            stallno1 = form.stallno.data

            
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()
            if stallnum:
                print stallnum.stallID
                print "hello2"
                sid__ = stallnum.stallID
                if stallnum.stall_status == "1":
                    flash("stall already Occupied")
                else:                        
                    tenantForm = Tenants(contact_no=Contnum,
                                         first_name=firstname,
                                         mid_name=middlename,
                                         last_name=lastname,
                                         present_addr=Address,
                                         stallID=sid__
                                         )
                    dbase.session.add(tenantForm)
                    dbase.session.commit()

                    stallnumm = Stalls.query.filter_by(stallID=stallnum.stallID).first()
                    stallnumm.stall_rate=form.rate.data
                    stallnumm.stall_status = "1"
                    print stallnumm.stallID
                    dbase.session.add(stallnumm)
                    dbase.session.commit()
                    
                    #else:
                    #    tyy = Tenants.query.filter_by(tenantID=storer).first()
                    #    tyy.tenant_photo = loc_default
                        #return render_template("addtenant.html", form1=form, availstalls = availstalls, availstalls_y=availstalls_y, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])
                    profile_entry = ""
                    te = Tenants.query.all()
                    tee = []
                    for et in te:
                        tee.append(et.tenantID)

                    storer = tee[len(tee)-1]
                    print storer
                    TenantphotoID = img_folder + str(storer)

                    rents = Rents(date_started=now, tenantID=storer, stallID=sid__)
                    dbase.session.add(rents)
                    dbase.session.commit()

                    if os.path.isdir(TenantphotoID) == False:
                        os.makedirs(TenantphotoID)

                    if form.tenantphotoID.data == None or form.tenantphotoID.data == "":
                        #tenants.tenant_photo = tenants.tenant_photo
                        tnore = Tenants.query.filter_by(tenantID=storer).first()
                        tnore.tenant_photo = loc_default
                        dbase.session.add(tnore)
                        dbase.session.commit()

                    else:
                        if form.tenantphotoID.data and allowed_file(form.tenantphotoID.data.filename):
                            filename = secure_filename(form.tenantphotoID.data.filename)
                            form.tenantphotoID.data.save(os.path.join(TenantphotoID + '/', filename))

                            uploadFolder = TenantphotoID + '/'
                            nameNew = str(int(time.time())) + '.' + str(os.path.splitext(filename)[1][1:])
                            os.rename(uploadFolder + filename, uploadFolder + nameNew)
                            profile_entry = uploadFolder+nameNew

                            t = Tenants.query.filter_by(tenantID=storer).first()
                            #t.tenant_photo = profile_entry
                            t.tenant_photo = 'static/profile/'+str(storer)+'/'+nameNew
                            print profile_entry
                            dbase.session.add(t)
                            user = current_user
                            lgdate= str(now)
                            msg = user.username + " added a tenant "
                            logmessage = Logs(details = msg,
                                                log_date = lgdate)
                            dbase.session.add(logmessage)
                            dbase.session.commit()

                    flash('Tenant added')
                    #return render_template("successadd1.html", result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])       
            else:
                flash("Stall not found")
    return render_template("addtenant.html", form1=form, availstalls = availstalls, availstalls_y=availstalls_y, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


@app.route("/AddTenants2", methods=["POST", "GET"])
@app.route("/AddTenants2/", methods=["POST", "GET"])
@login_required
@required_roles(1, 2)
def AddTenants2():
    form = addtenants()
    availstalls_y = []
    availstalls = Stalls.query.filter_by(stall_status= '0').all()#.paginate(1,11,True)
    for r in availstalls:
        type = Types.query.filter_by(typeID =r.typeID).first()
        availstalls_y.append(type.stall_type)

    x = []
    result = Tenants.query.order_by(Tenants.first_name).all()#.paginate(1,2,True)
    for r in result:
        stall = Stalls.query.filter_by(stallID=r.stallID).first()
        x.append(stall.stall_no)

    if request.method == "POST":
        print "scull"
        if form.validate_on_submit():
            print "hello1"
            firstname = form.fname.data
            middlename = form.mname.data
            lastname = form.lname.data
            Address = form.address.data
            Contnum = form.contnum.data
            TenantphotoID = form.tenantphotoID.data
            stallno1 = form.stallno.data

            
            stallnum = Stalls.query.filter_by(stall_no=stallno1).first()
            if stallnum:
                print stallnum.stallID
                print "hello2"
                sid__ = stallnum.stallID
                if stallnum.stall_status == "1":
                    flash("stall already Occupied")
                else:                        
                    tenantForm = Tenants(contact_no=Contnum,
                                         first_name=firstname,
                                         mid_name=middlename,
                                         last_name=lastname,
                                         present_addr=Address,
                                         stallID=sid__
                                         )
                    dbase.session.add(tenantForm)
                    dbase.session.commit()

                    stallnumm = Stalls.query.filter_by(stallID=stallnum.stallID).first()
                    stallnumm.stall_rate=form.rate.data
                    stallnumm.stall_status = "1"
                    print stallnumm.stallID
                    dbase.session.add(stallnumm)
                    dbase.session.commit()
                    
                    #else:
                    #    tyy = Tenants.query.filter_by(tenantID=storer).first()
                    #    tyy.tenant_photo = loc_default
                        #return render_template("addtenant.html", form1=form, availstalls = availstalls, availstalls_y=availstalls_y, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])
                    profile_entry = ""
                    te = Tenants.query.all()
                    tee = []
                    for et in te:
                        tee.append(et.tenantID)

                    storer = tee[len(tee)-1]
                    print storer
                    TenantphotoID = img_folder + str(storer)

                    rents = Rents(date_started=now, tenantID=storer, stallID=sid__)
                    dbase.session.add(rents)
                    dbase.session.commit()

                    if os.path.isdir(TenantphotoID) == False:
                        os.makedirs(TenantphotoID)

                    if form.tenantphotoID.data == None or form.tenantphotoID.data == "":
                        #tenants.tenant_photo = tenants.tenant_photo
                        tnore = Tenants.query.filter_by(tenantID=storer).first()
                        tnore.tenant_photo = loc_default
                        dbase.session.add(tnore)
                        dbase.session.commit()

                    else:
                        if form.tenantphotoID.data and allowed_file(form.tenantphotoID.data.filename):
                            filename = secure_filename(form.tenantphotoID.data.filename)
                            form.tenantphotoID.data.save(os.path.join(TenantphotoID + '/', filename))

                            uploadFolder = TenantphotoID + '/'
                            nameNew = str(int(time.time())) + '.' + str(os.path.splitext(filename)[1][1:])
                            os.rename(uploadFolder + filename, uploadFolder + nameNew)
                            profile_entry = uploadFolder+nameNew

                            t = Tenants.query.filter_by(tenantID=storer).first()
                            #t.tenant_photo = profile_entry
                            t.tenant_photo = 'static/profile/'+str(storer)+'/'+nameNew
                            print profile_entry
                            dbase.session.add(t)
                            user = current_user
                            lgdate= str(now)
                            msg = user.username + " added a tenant "
                            logmessage = Logs(details = msg,
                                                log_date = lgdate)
                            dbase.session.add(logmessage)
                            dbase.session.commit()

                    flash('Tenant added')
                    #return render_template("successadd1.html", result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])       
            else:
                flash("Stall not found")
    return render_template("clerk_addtenant.html", form1=form, availstalls = availstalls, availstalls_y=availstalls_y, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


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
                flash("Stall Added!!")
                #return render_template("addstall.html", form=form, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])
                #return render_template("successadd1.html", result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])
    return render_template("addstall.html", form=form, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])



@app.route("/clerk", methods = ["POST", "GET" ])
@app.route("/clerk/", methods = ["POST", "GET" ])
# @login_required
# @required_roles(1)
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
                            roleID = '2'
                            )
            regclerk = Users.query.filter_by(username=form.username.data).first()
            if regclerk:
                flash('username is already used')
                print "l"
            else:     
                dbase.session.add(uForm)
                user = current_user
                lgdate= str(now)
                msg = user.username + " added a clerk "
                logmessage = Logs(details = msg,
                                    log_date = lgdate)
                dbase.session.add(logmessage)
                dbase.session.commit()
                flash('Clerk added!')
                #return render_template('successadd1.html', result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])
    return render_template("addclerk.html", form=form, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


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
                    #return '<h1>Invalid username or password!</h1>'
                    flash('Invalid username or password')
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
                        flash('You were log in')
                        return redirect(url_for('index2'))
                    #return '<h1>Invalid username or password!</h1>'
                    flash('Invalid username or password')

                else:
                    #return '<h1>Invalid username or password!</h1>'
                    flash('Invalid username or password')
            else:
                #return '<h1>Invalid username or password!</h1>'
                flash('Invalid username or password')
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
    x1 = []  
    result_tenants = Tenants.query.order_by(Tenants.first_name).all()#.paginate(1,2,True)
    
    for r in result_tenants:        
        stall = Stalls.query.filter_by(stallID=r.stallID).first()
        x1.append(stall.stall_no)

    return render_template('showtenants.html',result_tenants=result_tenants, x1=x1, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])

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
    x1 = []
    result_stall = Stalls.query.order_by(Stalls.stall_no).all()#.paginate(1,11,True)
    for r in result_stall:
        tayp = Types.query.filter_by(typeID =r.typeID).first()
        x1.append(tayp.stall_type)
    return render_template('showstalls.html', result_stall=result_stall, x1=x1, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])

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
    return render_template('logs.html', showlogs=showlogs, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


@app.route('/payment_table/<int:id>/<int:s_id>/', methods = ["GET", "POST"])
@login_required
@required_roles(1,2)
def paymenttable(id, s_id):
    pays = Pays.query.filter(and_(Pays.tenantID==id, Pays.stallID==s_id)).all()
    someNum = Stalls.query.filter_by(stallID=s_id).first()
    tenant_1 = Tenants.query.filter(and_(Tenants.tenantID==id, Tenants.stallID==someNum.stallID)).first()
    typee = Types.query.filter_by(typeID=someNum.typeID).first()
    form= PaymentForm()

    remark_re=""
    if form.remark.data=='1':
        remark_re = 'Advance'
    elif form.remark.data=='2':
        remark_re = 'Full'
    elif form.remark.data=='3':
        remark_re = 'Partial'


    if request.method=='POST' and form.validate_on_submit():
        uForms = Pays(month=form.month.data,
                        amount=form.amount.data,
                        sCharge=form.sCharge.data,
                        total=form.total.data ,
                        or_no=form.or_no.data,
                        date_issued=now,
                        issued_by=form.issued_by.data,
                        tenantID = tenant_1.tenantID,
                        stallID = someNum.stallID,
                        remark = remark_re
                       )

        dbase.session.add(uForms)
        dbase.session.commit()
        return redirect(url_for("paymenttable", id=id, s_id=s_id))
    if current_user.roleID == 1:
        return render_template('paymenttable_admin.html', form=form, pays=pays, id=id, s_id=s_id, stall=someNum, typee=typee, tenant=tenant_1, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])
    return render_template('paymenttable.html', form =form, pays=pays, id=id, s_id=s_id, stall=someNum, typee=typee, tenant=tenant_1, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


@app.route('/payment')
@app.route('/payment/')
@login_required
@required_roles(1,2)
def payment():
    form= PaymentForm()
    tenant = Tenants.query.filter_by(tenant_status='1').all()
    return render_template('payment.html', form=form, tenn=tenant, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])


@app.route('/edit_tenant/<int:id>/<int:s_id>', methods=["GET", "POST"])
@login_required
@required_roles(1,2)
def edit_tenant(id, s_id):
    form = edit_tenant_form()
    tenant = Tenants.query.filter_by(tenantID=id).first()
    if request.method=='POST':
        if form.validate_on_submit():
            tenant.first_name = form.fname.data
            tenant.mid_name = form.mname.data
            tenant.last_name = form.lname.data
            tenant.present_addr = form.address.data
            tenant.contact_no = form.contnum.data


            dbase.session.add(tenant)
            dbase.session.commit()

            #pays = Pays.query.filter(and_(Pays.tenantID==id, Pays.stallID==s_id)).all()
            #return render_template('tenantprofile.html', pays=pays, id=id, s_id=s_id)
            flash('Success!')
        else:
            flash('Something went wrong!')

    else:
        form.fname.data = tenant.first_name
        form.mname.data = tenant.mid_name
        form.lname.data = tenant.last_name
        form.address.data = tenant.present_addr
        form.contnum.data = tenant.contact_no

    return render_template('edit_tenant.html', form1=form, tenant=tenant)

@app.route("/alternate/payment")
def select_tenant():
    tenant = Tenants.query.filter_by(tenantID=int(request.args.get('tenant_id'))).first()
    stall = Stalls.query.filter_by(stallID=int(request.args.get('stall_id'))).first()
    type = Types.query.filter_by(typeID=stall.typeID).first()
    pays = Pays.query.filter(and_(Pays.tenantID==tenant.tenantID, Pays.stallID==stall.stallID)).first()
    name = str(tenant.last_name)+', '+str(tenant.first_name)+' '+str(tenant.mid_name)
    return jsonify(prof= tenant.tenant_photo, name = name, cnum = tenant.contact_no, addr = tenant.present_addr, stallnum = stall.stall_no, stallloc = stall.stall_loc, stalltype = type.stall_type, rate = stall.stall_rate, balance= 0)

@app.route('/alternate/payment/transac')
def pay_tenant():
    list = []

    list.append(request.args.get('amount'))
    list.append(request.args.get('scharge'))
    list.append(request.args.get('month'))
    list.append(request.args.get('total'))
    list.append(request.args.get('or_no'))
    list.append(request.args.get('issued_by'))
    list.append(request.args.get('tenant_id'))
    list.append(request.args.get('stall_id'))

    count=0
    for r in list:
        if r==None or r=="":
            count=count+1
            break

    remark_re =""
    remark_state = request.args.get('remark')

    if remark_state=='1':
        remark_re = 'Advance'
    elif remark_state=='2':
        remark_re = 'Full'
    elif remark_state=='3':
        remark_re = 'Partial'


    if count==0:
        uForms = Pays(month=request.args.get('month'),
            amount=float(request.args.get('amount')),
            sCharge=float(request.args.get('scharge')),
            total=float(request.args.get('total')),
            or_no=request.args.get('or_no'),
            date_issued=now,
            issued_by=request.args.get('issued_by'),
            tenantID =int(request.args.get('tenant_id')),
            stallID =int(request.args.get('stall_id')),
            remark=remark_re
       )

        dbase.session.add(uForms)
        dbase.session.commit()
        return jsonify(msg='payment added!')
    return jsonify(msg='missing input!')

@app.route('/evict_tenant/<int:id>/<int:s_id>')
def evict_tenant(id,s_id):
    etanant = Tenants.query.filter(and_(Tenants.tenantID==id, Tenants.stallID == s_id)).first()
    estall =Stalls.query.filter_by(stallID=s_id).first()
    if etanant.tenant_status =='1':
        etanant.tenant_status = '0'
        dbase.session.add(etanant)
        dbase.session.commit()

        estall.stall_status = '0'
        dbase.session.add(estall)
        dbase.session.commit()
        flash('Tenant Evicted')

    x1 = []  
    result_tenants = Tenants.query.order_by(Tenants.first_name).all()#.paginate(1,2,True)
    
    for r in result_tenants:        
        stall = Stalls.query.filter_by(stallID=r.stallID).first()
        x1.append(stall.stall_no)
    return render_template('showtenants.html', result_tenants=result_tenants, x1=x1, result=search_panel(0)[0], x=search_panel(0)[1], result2=search_panel(1)[0], y=search_panel(1)[1])

@app.route('/notifications')
def notify():
    curmonth = now

    tenact = Tenants.query.filter_by(tenant_status ='1').all()
    for t in tenact:
        tpays = Pays.query.filter(and_(tenantID==t.tenantID, stallID==t.stallID)).order_by(Pays.paysID.desc()).first()
        print tpays.date_issued
    print "dsadjasjfkjab"
    return render_template('showtenants.html')


