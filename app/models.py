from app import dbase


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

class Stalls(dbase.Model):
    __tablename__ = 'stalls'
    stallID = dbase.Column(dbase.Integer, primary_key=True)
    stall_rate = dbase.Column(dbase.Float)
    stall_loc = dbase.Column(dbase.String(60))
    stall_status = dbase.Column(dbase.String(60))
    branchID = dbase.Column(dbase.Integer, dbase.ForeignKey("branch.branchID"), nullable=False)

    def __init__ (self,stall_rate, stall_loc, stall_status, branchID):
        self.stall_rate =stall_rate
        self.stall_status = stall_status
        self.stall_loc = stall_loc
        self.branchID = branchID

    def __repr__(self):
        return '<stall_rate{}>'.format(self.stall_rate)

class Users(dbase.Model):
    __tablename__ ="users"
    userID = dbase.Column(dbase.Integer,primary_key= True)
    roleID = dbase.Column(dbase.Integer)
    username = dbase.Column(dbase.String(20), unique=True)
    passwrd = dbase.Column(dbase.String(20))
    contact_no = dbase.Column(dbase.String(12))
    first_name = dbase.Column(dbase.String(24))
    mid_name = dbase.Column(dbase.String(24))
    last_name = dbase.Column(dbase.String(24))
    branchID = dbase.Column(dbase.Integer, dbase.ForeignKey("branch.branchID"), nullable=False)

    def __init__(self, roleID, username,passwrd,contact_no,first_name,mid_name,last_name,branchID):
        self.roleID = roleID
        self.username = username
        self.passwrd = passwrd
        self.first_name = first_name
        self.mid_name= mid_name
        self.last_name= last_name
        self.contact_no = contact_no
        self.branchID = branchID

    def __repr__(self):
        return '<roleID {}>'.format(self.roleID)

class Tenants(dbase.Model):
    __tablename__ = "tenants"
    tenantID = dbase.Column(dbase.Integer, primary_key= True)
    contact_no = dbase.Column(dbase.String(12))
    first_name = dbase.Column(dbase.String(24))
    mid_name = dbase.Column(dbase.String(24))
    last_name = dbase.Column(dbase.String(24))
    present_addr = dbase.Column(dbase.String(60))
    tenant_photo = dbase.Column(dbase.String(60))
    stallID = dbase.Column(dbase.Integer, dbase.ForeignKey("stalls.stallID"), nullable=True)

    def __init__(self,contact_no, first_name, mid_name, last_name, present_addr, tenant_photo, stallID):
        self.first_name = first_name
        self.mid_name = mid_name
        self.last_name = last_name
        self.contact_no = contact_no
        self.present_addr = present_addr
        self.tenant_photo = tenant_photo
        self.stallID = stallID

    def __repr__(self):
        return '<last_name {}>'.format(self.last_name)

class Logs(dbase.Model):
    __tablename__ = "logs"
    logID = dbase.Column(dbase.Integer, primary_key=True)
    details = dbase.Column(dbase.String(60))
    log_date =dbase.Column(dbase.String(60))
    branchID = dbase.Column(dbase.Integer,dbase.ForeignKey("branch.branchID"), nullable=True)

    def __init__(self, details, log_date, branchID):
        self.details = details
        self.log_date = log_date
        self.branchID = branchID

    def __repr__(self):
        return '<details{}>'.format(self.branchID)


class Pays(dbase.Model):
    __tablename__ = "pays"
    paysID = dbase.Column(dbase.Integer, primary_key=True)
    issued_by = dbase.Column(dbase.String(60))
    reference_no = dbase.Column(dbase.String(60))
    or_no = dbase.Column(dbase.String(60))
    rent = dbase.Column(dbase.Float)
    sCharge = dbase.Column(dbase.Float)
    tenantID = dbase.Column(dbase.Integer,dbase.ForeignKey("tenants.tenantID"), nullable=True)
    stallID = dbase.Column(dbase.Integer, dbase.ForeignKey("stalls.stallID"), nullable=True)

    def __init__(self, issued_by, reference_no,or_no,rent,sCharge, tenantID, stalID):
        self.issued_by = issued_by
        self.or_no = or_no
        self.rent = rent
        self.sCharge = sCharge
        self.tenantID = tenantID
        self.stallID = stalID


    def __repr__(self):
        return '< issued_by{}>'.format(self.issued_by)

