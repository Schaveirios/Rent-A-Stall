from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, SubmitField, SelectField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired,Length


class addtenants(Form):

    fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=2,max=20)])
    mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=2,max=20)])
    lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=2,max=20)])
    address = StringField('Present Address', [validators.Length(min=5,max=50)])
    stalltype = StringField('stall type', [validators.Length(min=5,max=50)])
    contnum = StringField('Contact Number', [validators.Length(min=11,max=11)])
    stallno = StringField('Stall Number',[validators.DataRequired(),validators.Length(min=1,max=20)])
    tenantphotoID = FileField('TenantphotoID')
    stallloc = StringField('Stall type',[validators.DataRequired(),validators.Length(max=20)])
    branch = SelectField(u'branches', choices=[('1', 'Tambo'), ('2', 'Pala-o'), ('3', 'wet market')])
    submit = SubmitField("Submit")



class addstalls(Form):

    stallno = IntegerField('stallno',[validators.DataRequired(),validators.Length(max=20)])
    stallloc = StringField('stallloc',[validators.DataRequired(),validators.Length(max=20)])
    rate = IntegerField('rate',[validators.DataRequired(),validators.Length(max=20)])
    Branchloc = SelectField(u'branches', choices=[('1', 'Tambo'), ('2', 'Pala-o'), ('3', 'wet market')])
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

class addbranch(Form):

    location = StringField('location',[validators.DataRequired(),validators.Length(min=6,max=20)])

    submit = SubmitField("Submit")

class LogIn(Form):

    username = StringField('Username',[validators.DataRequired(),validators.Length(min=6,max=20)])
    passwrd = PasswordField('Password ',[validators.DataRequired(),validators.Length(min=6,max=20)])

    submit = SubmitField("Login")

class RegisterForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=3, max=15)])
    mname =  StringField('Middle Name', validators=[InputRequired(), Length(min=4, max=15)])
    lname =  StringField('Last Name', validators=[InputRequired(), Length(min=2, max=15)])
    ContNum =  StringField('Contact Number', validators=[InputRequired(), Length(min=11, max=15)])
    branchID = SelectField(u'branches', choices=[('1', 'Tambo'), ('2', 'Palao'), ('3', 'Central Market')])
