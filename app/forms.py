from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired



class Tenants(Form):

<<<<<<< HEAD
	fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=6,max=20)])
	mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=6,max=20)])
	lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=6,max=20)])
=======
	sname = StringField('Surename',[validators.DataRequired(),validators.Length(min=6,max=20)])
	mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=6,max=20)])
	fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=6,max=20)])
	mname = StringField('Midlename',[validators.DataRequired(),validators.Length(min=6,max=20)])
    lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=6,max=20)])
>>>>>>> bc249a4861ee229e7a43bc00dcfe642e873aea91
    Address = StringField('Present Address', [validators.Length(min=10,max=50)])
    ContNum = StringField('Contact Number', [validators.Length(min=10,max=50)])
    stallno = StringField('Stall Number',[validators.DataRequired(),validators.Length(min=6,max=20)])
    TenantphotoID = FileField('TenantphotoID')
    submit = SubmitField("Submit")


class Stalls(Form):

	stallno = StringField('stallno',[validators.DataRequired(),validators.Length(min=6,max=20)])
	stallloc = StringField('stallloc',[validators.DataRequired(),validators.Length(min=6,max=20)])
    rate = StringField('rate',[validators.DataRequired(),validators.Length(min=6,max=20)])
    location = StringField('location',[validators.DataRequired(),validators.Length(min=6,max=20)])

    submit = SubmitField("Submit")

class User(Form):

    uname = StringField('Username',[validators.DataRequired(),validators.Length(min=6,max=20)])
    fname = StringField('Firstname',[validators.DataRequired(),validators.Length(min=6,max=20)])
    mname = StringField('Middlename',[validators.DataRequired(),validators.Length(min=6,max=20)])
    lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=6,max=20)])
    password = StringField('Password', [validators.Length(min=10,max=50)])
    ContNum = StringField('Contact Number', [validators.Length(min=10,max=50)])
        
    submit = SubmitField("Submit")

class Branch(Form):

    location = StringField('location',[validators.DataRequired(),validators.Length(min=6,max=20)])

    submit = SubmitField("Submit")

