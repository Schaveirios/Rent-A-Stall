from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, SubmitField, SelectField, IntegerField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired,Length


class addtenants(Form):

    fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=2,max=20)])
    mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=2,max=20)])
    lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=2,max=20)])
    address = StringField('Present Address', [validators.Length(min=5,max=50)])
    #stalltype = StringField('stall type', [validators.Length(min=5,max=50)])
    contnum = StringField('Contact Number', [validators.Length(min=11,max=11)])
    stallno = StringField('Stall Number',[validators.DataRequired(),validators.Length(min=1,max=20)])
    rate = StringField('Stall Rate',[validators.DataRequired(),validators.Length(min=1,max=20)])
    tenantphotoID = FileField('TenantphotoID')
    #stallloc = StringField('Stall type',[validators.DataRequired(),validators.Length(max=20)])
    #status = SelectField('Status', choices=[('1', 'Active'), ('0', 'Inactive')])
    #branch = StringField(u'branches',[validators.DataRequired(),validators.Length(max=10)])
    submit = SubmitField("Submit")
    # status = RadioField('Approval Status',[validators.DataRequired()],choices=[('1','Approved'),('0','Pending')])



class addstalls(Form):

    stallno = StringField('stallno',[validators.DataRequired(),validators.Length(max=20)])
    stallloc = StringField('stallloc',[validators.DataRequired(),validators.Length(max=20)])
    rate = StringField('rate',[validators.DataRequired(),validators.length(max=20)])
    stalltype = StringField('Stall type',[validators.DataRequired(),validators.Length(max=20)])
    submit = SubmitField("Add")

# class addclerk(Form):

#     uname = StringField('Username',[validators.DataRequired(),validators.Length(min=6,max=20)])
#     fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=2,max=20)])
#     mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=5,max=20)])
#     lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=5,max=20)])
#     password = PasswordField('Password', [validators.Length(min=10,max=50)])
#     ContNum = StringField('Contact Number', [validators.Length(min=10,max=50)])
#     branchId = SelectField(u'branches', choices=[('1', 'Tambo'), ('2', 'Pala-o'), ('3', 'wet market')])
#     submit = SubmitField("Add")

# class addbranch(Form):

#     location = StringField('location',[validators.DataRequired(),validators.Length(min=6,max=20)])

#     submit = SubmitField("Submit")

class LogIn(Form):

    username = StringField('Username',[validators.DataRequired(),validators.Length(min=5,max=20)])
    passwrd = PasswordField('Password ',[validators.DataRequired(),validators.Length(min=6,max=20)])

    submit = SubmitField("Login")

class RegisterForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=3, max=15)])
    mname =  StringField('Middle Name', validators=[InputRequired(), Length(min=4, max=15)])
    lname =  StringField('Last Name', validators=[InputRequired(), Length(min=2, max=15)])
    ContNum =  StringField('Contact Number', validators=[InputRequired(), Length(min=11, max=15)])
    # branchID = StringField('branches',[validators.DataRequired(),validators.Length(max=20)])
    submit = SubmitField("Add")
	
class PaymentForm(Form):
#    month = StringField('Month', validators=[InputRequired(), Length(min=1, max=64)])
    month = SelectField('Month', choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')])
    amount = StringField('Amount', validators=[InputRequired(), Length(min=1, max=64)])
    sCharge = StringField('S. Charge', validators=[InputRequired(), Length(min=1, max=64)])
    total = StringField('Total', validators=[InputRequired(), Length(min=1, max=64)])
    or_no = StringField('OR Num', validators=[InputRequired(), Length(min=1, max=64)])
    # date_issued = StringField('Date Issued', validators=[InputRequired(), Length(min=3, max=64)])
    issued_by = StringField('Issued By', validators=[InputRequired(), Length(min=4, max=64)])
    remark = SelectField('Remarks', choices=[('1', 'Advance'), ('2', 'Full'), ('3', 'Partial')])
    submit = SubmitField("Submit")

class edit_tenant_form(Form):
    fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=2,max=20)])
    mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=2,max=20)])
    lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=2,max=20)])
    address = StringField('Present Address', [validators.Length(min=5,max=50)])
    contnum = StringField('Contact Number', [validators.Length(min=11,max=11)])
    submit = SubmitField("Submit")
