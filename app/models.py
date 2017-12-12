from app import dbase
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from app import app
from flask_login import AnonymousUserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from datetime import datetime

class Branch(dbase.Model):
    __tablename__ = "branch"
    branchID = dbase.Column(dbase.Integer, primary_key= True)
    branch_loc = dbase.Column(dbase.String(60))
    branch_logo = dbase.Column(dbase.String(60))

    def __init__(self, branch_loc, branch_logo):
        self.branch_loc = branch_loc
        self.branch_logo = branch_logo

    def __repr__(self):
        return '<branch_loc {}>'.format(self.branch_loc)

    @staticmethod
    def branch_types():
        brLoc = ['Palao']
        for b in brLoc:
            loc = Branch.query.filter_by(branch_loc = b).first()
            if loc is None:
                loc = Branch(branch_loc= b, branch_logo='Default')
            dbase.session.add(loc)
        dbase.session.commit()


class Stalls(dbase.Model):
    __tablename__ = 'stalls'
    stallID = dbase.Column(dbase.Integer, primary_key=True, autoincrement= True)
    stall_no = dbase.Column(dbase.Integer)
    stall_rate = dbase.Column(dbase.Integer)
    stall_loc = dbase.Column(dbase.String(60))
    stall_status = dbase.Column(dbase.String(60))
    typeID = dbase.Column(dbase.Integer, dbase.ForeignKey("types.typeID"), nullable= False)
    # branchID = dbase.Column(dbase.Integer, dbase.ForeignKey("branch.branchID"), nullable=False)
    t_stall_no = relationship("Tenants", backref="stallNO", lazy="dynamic" )
    def __init__ (self,stall_rate, stall_loc, stall_status, stall_no, typeID):
        self.stall_rate =stall_rate
        self.stall_status = '0'
        self.stall_loc = stall_loc
        self.stall_no = stall_no
        # self.branchID = branchID
        self.typeID = typeID

    def __repr__(self):
        return '<stall_rate{}>'.format(self.stall_rate)
        

class Users(dbase.Model):
    __tablename__ ="users"
    userID = dbase.Column(dbase.Integer,primary_key= True, autoincrement= True)
    roleID = dbase.Column(dbase.Integer)
    username = dbase.Column(dbase.String(20), unique=True)
    passwrd = dbase.Column(dbase.String(255))
    contact_no = dbase.Column(dbase.String(12))
    first_name = dbase.Column(dbase.String(24))
    mid_name = dbase.Column(dbase.String(24))
    last_name = dbase.Column(dbase.String(24))
    # branchID = dbase.Column(dbase.Integer, dbase.ForeignKey("branch.branchID"), nullable=False)

    def __init__(self, roleID, username,passwrd,contact_no,first_name,mid_name,last_name):
        self.roleID = roleID
        self.username = username
        self.passwrd = generate_password_hash(passwrd)
        self.first_name = first_name
        self.mid_name= mid_name
        self.last_name= last_name
        self.contact_no = contact_no
        # self.branchID = branchID


    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def getRole_id(self):
        return self.roleID

    def get_id(self):
        return self.userID

    def __repr__(self):
        return '<roleID {}>'.format(self.roleID)

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return Users.query.get(id)
        return None

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

    def isAuthenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return True



class Tenants(dbase.Model):
    __tablename__ = "tenants"
    tenantID = dbase.Column(dbase.Integer, primary_key= True, autoincrement=True)
    contact_no = dbase.Column(dbase.String(12))
    first_name = dbase.Column(dbase.String(24))
    mid_name = dbase.Column(dbase.String(24))
    last_name = dbase.Column(dbase.String(24))
    present_addr = dbase.Column(dbase.String(60))
    tenant_photo = dbase.Column(dbase.String(60))
    stallID = dbase.Column(dbase.Integer, dbase.ForeignKey("stalls.stallID"), nullable=True)

    def __init__(self,contact_no, first_name, mid_name, last_name, present_addr, stallID):
        self.first_name = first_name
        self.mid_name = mid_name
        self.last_name = last_name
        self.contact_no = contact_no
        self.present_addr = present_addr
        self.stallID = stallID


    def __repr__(self):
        return '<last_name {}>'.format(self.last_name)

class Logs(dbase.Model):
    __tablename__ = "logs"
    logID = dbase.Column(dbase.Integer, primary_key=True, autoincrement=True)
    details = dbase.Column(dbase.String(60))
    log_date =dbase.Column(dbase.DateTime)

    def __init__(self, details, log_date):
        self.details = details
        self.log_date = log_date

    def __repr__(self):
        return '<details{}>'.format(self.logID)


class Pays(dbase.Model):
    __tablename__ = "pays"
    paysID = dbase.Column(dbase.Integer, primary_key=True, autoincrement= True)
    issued_by = dbase.Column(dbase.String(60))
    reference_no = dbase.Column(dbase.String(60))
    or_no = dbase.Column(dbase.String(60))
    # rent = dbase.Column(dbase.Float)
    sCharge = dbase.Column(dbase.Float)
    month = dbase.Column(dbase.String(20))
    amount = dbase.Column(dbase.Float)
    total = dbase.Column(dbase.Float)
    date_issued =dbase.Column(dbase.DATE)
    tenantID = dbase.Column(dbase.Integer,dbase.ForeignKey("tenants.tenantID"), nullable=True)
    stallID = dbase.Column(dbase.Integer, dbase.ForeignKey("stalls.stallID"), nullable=True)

    def __init__(self, issued_by,or_no,sCharge, tenantID, stallID,month, amount,total,date_issued):
        self.issued_by = issued_by
        self.or_no = or_no
        # self.rent = rent
        self.sCharge = sCharge
        self.tenantID = tenantID
        self.stallID = stallID
        self.month = month
        self.amount = amount
        self.total = total
        self.date_issued = date_issued

    def __repr__(self):
        return '< issued_by{}>'.format(self.issued_by)


class Rents(dbase.Model):
    __tablename__ = "rents"
    rentID = dbase.Column(dbase.Integer, primary_key=True)
    date_started = dbase.Column(dbase.DATE)
    tenantID = dbase.Column(dbase.Integer,dbase.ForeignKey("tenants.tenantID"), nullable=True)
    stallID = dbase.Column(dbase.Integer, dbase.ForeignKey("stalls.stallID"), nullable=True)

    def __index__(self,date_started, tenantID, stallID):
        self.date_started = date_started
        self.tenantID = tenantID
        self.stallID = stallID

    def __repr__(self):
        return '<date_started{}>'.format(self.date_started)

class Types(dbase.Model):
    __tablename__ = 'types'
    typeID = dbase.Column(dbase.Integer, primary_key=True, autoincrement= True)
    stall_type = dbase.Column(dbase.String(60))


    def __index__(self, stall_type):
        self.stall_type = stall_type

    def __repr__(self):
        return '<stall_type{}>'.format(self.stall_type)

    @staticmethod
    def stall_types():
        stypes = ['Carenderia', 'Stall2', 'Stall3']
        for s in stypes:
            tyype = Types.query.filter_by(stall_type = s).first()
            if tyype is None:
                tyype = Types(stall_type= s)
            dbase.session.add(tyype)
        dbase.session.commit()
