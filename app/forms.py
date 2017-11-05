from flask_wtf import Form
from wtforms import StringField, PasswordField, validators, SubmitField

class Tenants(Form):

	sname = StringField('Surename',[validators.DataRequired(),validators.Length(min=6,max=20)])
	mname = StringField('Midlename',[validators.DataRequired(),validators.Length(min=6,max=20)])
    lname = StringField('Lastname',[validators.DataRequired(),validators.Length(min=6,max=20)])
    Address = StringField('Present Address', [validators.Length(min=10,max=50)])
    ContNum = StringField('Contact Number', [validators.Length(min=10,max=50)])
    stallno = StringField('Stall Number',[validators.DataRequired(),validators.Length(min=6,max=20)])
    submit = SubmitField("Submit")


class Stalls(Form):

	stallno = StringField('stallno',[validators.DataRequired(),validators.Length(min=6,max=20)])
	stallloc = StringField('stallloc',[validators.DataRequired(),validators.Length(min=6,max=20)])
    rate = StringField('rate',[validators.DataRequired(),validators.Length(min=6,max=20)])
    
    submit = SubmitField("Submit")