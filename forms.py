from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, widgets, HiddenField,TextAreaField
from wtforms.validators import DataRequired, InputRequired, EqualTo

stateChoices = [
        ('AK', 'Alaska'),
        ('AL', 'Alabama'),
        ('AR', 'Arkansas'),
        ('AS', 'American Samoa'),
        ('AZ', 'Arizona'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DC', 'District of Columbia'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('GU', 'Guam'),
        ('HI', 'Hawaii'),
        ('IA', 'Iowa'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('MA', 'Massachusetts'),
        ('MD', 'Maryland'),
        ('ME', 'Maine'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MO', 'Missouri'),
        ('MP', 'Northern Mariana Islands'),
        ('MS', 'Mississippi'),
        ('MT', 'Montana'),
        ('NA', 'National'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('NE', 'Nebraska'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NV', 'Nevada'),
        ('NY', 'New York'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VA', 'Virginia'),
        ('VI', 'Virgin Islands'),
        ('VT', 'Vermont'),
        ('WA', 'Washington'),
        ('WI', 'Wisconsin'),
        ('WV', 'West Virginia'),
        ('WY', 'Wyoming')
]

countryChoices=[
    ("United States","United States"),
    ("Afghanistan","Afghanistan"),
    ("Albania","Albania"),
    ("Algeria","Algeria"),
    ("Andorra","Andorra"),
    ("Angola","Angola"),
    ("Antigua & Deps","Antigua & Deps"),
    ("Argentina","Argentina"),
    ("Armenia","Armenia"),
    ("Australia","Australia"),
    ("Austria","Austria"),
    ("Azerbaijan","Azerbaijan"),
    ("Bahamas","Bahamas"),
    ("Bahrain","Bahrain"),
    ("Bangladesh","Bangladesh"),
    ("Barbados","Barbados"),
    ("Belarus","Belarus"),
    ("Belgium","Belgium"),
    ("Belize","Belize"),
    ("Benin","Benin"),
    ("Bhutan","Bhutan"),
    ("Bolivia","Bolivia"),
    ("Bosnia Herzegovina","Bosnia Herzegovina"),
    ("Botswana","Botswana"),
    ("Brazil","Brazil"),
    ("Brunei","Brunei"),
    ("Bulgaria","Bulgaria"),
    ("Burkina","Burkina"),
    ("Burundi","Burundi"),
    ("Cambodia","Cambodia"),
    ("Cameroon","Cameroon"),
    ("Canada","Canada"),
    ("Cape Verde","Cape Verde"),
    ("Central African Rep","Central African Rep"),
    ("Chad","Chad"),
    ("Chile","Chile"),
    ("China","China"),
    ("Colombia","Colombia"),
    ("Comoros","Comoros"),
    ("Congo","Congo"),
    ("Congo {Democratic Rep}","Congo {Democratic Rep}"),
    ("Costa Rica","Costa Rica"),
    ("Croatia","Croatia"),
    ("Cuba","Cuba"),
    ("Cyprus","Cyprus"),
    ("Czech Republic","Czech Republic"),
    ("Denmark","Denmark"),
    ("Djibouti","Djibouti"),
    ("Dominica","Dominica"),
    ("Dominican Republic","Dominican Republic"),
    ("East Timor","East Timor"),
    ("Ecuador","Ecuador"),
    ("Egypt","Egypt"),
    ("El Salvador","El Salvador"),
    ("Equatorial Guinea","Equatorial Guinea"),
    ("Eritrea","Eritrea"),
    ("Estonia","Estonia"),
    ("Ethiopia","Ethiopia"),
    ("Fiji","Fiji"),
    ("Finland","Finland"),
    ("France","France"),
    ("Gabon","Gabon"),
    ("Gambia","Gambia"),
    ("Georgia","Georgia"),
    ("Germany","Germany"),
    ("Ghana","Ghana"),
    ("Greece","Greece"),
    ("Grenada","Grenada"),
    ("Guatemala","Guatemala"),
    ("Guinea","Guinea"),
    ("Guinea-Bissau","Guinea-Bissau"),
    ("Guyana","Guyana"),
    ("Haiti","Haiti"),
    ("Honduras","Honduras"),
    ("Hungary","Hungary"),
    ("Iceland","Iceland"),
    ("India","India"),
    ("Indonesia","Indonesia"),
    ("Iran","Iran"),
    ("Iraq","Iraq"),
    ("Ireland {Republic}","Ireland {Republic}"),
    ("Israel","Israel"),
    ("Italy","Italy"),
    ("Ivory Coast","Ivory Coast"),
    ("Jamaica","Jamaica"),
    ("Japan","Japan"),
    ("Jordan","Jordan"),
    ("Kazakhstan","Kazakhstan"),
    ("Kenya","Kenya"),
    ("Kiribati","Kiribati"),
    ("Korea North","Korea North"),
    ("Korea South","Korea South"),
    ("Kosovo","Kosovo"),
    ("Kuwait","Kuwait"),
    ("Kyrgyzstan","Kyrgyzstan"),
    ("Laos","Laos"),
    ("Latvia","Latvia"),
    ("Lebanon","Lebanon"),
    ("Lesotho","Lesotho"),
    ("Liberia","Liberia"),
    ("Libya","Libya"),
    ("Liechtenstein","Liechtenstein"),
    ("Lithuania","Lithuania"),
    ("Luxembourg","Luxembourg"),
    ("Macedonia","Macedonia"),
    ("Madagascar","Madagascar"),
    ("Malawi","Malawi"),
    ("Malaysia","Malaysia"),
    ("Maldives","Maldives"),
    ("Mali","Mali"),
    ("Malta","Malta"),
    ("Marshall Islands","Marshall Islands"),
    ("Mauritania","Mauritania"),
    ("Mauritius","Mauritius"),
    ("Mexico","Mexico"),
    ("Micronesia","Micronesia"),
    ("Moldova","Moldova"),
    ("Monaco","Monaco"),
    ("Mongolia","Mongolia"),
    ("Montenegro","Montenegro"),
    ("Morocco","Morocco"),
    ("Mozambique","Mozambique"),
    ("Myanmar, {Burma}","Myanmar, {Burma}"),
    ("Namibia","Namibia"),
    ("Nauru","Nauru"),
    ("Nepal","Nepal"),
    ("Netherlands","Netherlands"),
    ("New Zealand","New Zealand"),
    ("Nicaragua","Nicaragua"),
    ("Niger","Niger"),
    ("Nigeria","Nigeria"),
    ("Norway","Norway"),
    ("Oman","Oman"),
    ("Pakistan","Pakistan"),
    ("Palau","Palau"),
    ("Panama","Panama"),
    ("Papua New Guinea","Papua New Guinea"),
    ("Paraguay","Paraguay"),
    ("Peru","Peru"),
    ("Philippines","Philippines"),
    ("Poland","Poland"),
    ("Portugal","Portugal"),
    ("Qatar","Qatar"),
    ("Romania","Romania"),
    ("Russian Federation","Russian Federation"),
    ("Rwanda","Rwanda"),
    ("St Kitts & Nevis","St Kitts & Nevis"),
    ("St Lucia","St Lucia"),
    ("Saint Vincent & the Grenadines","Saint Vincent & the Grenadines"),
    ("Samoa","Samoa"),
    ("San Marino","San Marino"),
    ("Sao Tome & Principe","Sao Tome & Principe"),
    ("Saudi Arabia","Saudi Arabia"),
    ("Senegal","Senegal"),
    ("Serbia","Serbia"),
    ("Seychelles","Seychelles"),
    ("Sierra Leone","Sierra Leone"),
    ("Singapore","Singapore"),
    ("Slovakia","Slovakia"),
    ("Slovenia","Slovenia"),
    ("Solomon Islands","Solomon Islands"),
    ("Somalia","Somalia"),
    ("South Africa","South Africa"),
    ("South Sudan","South Sudan"),
    ("Spain","Spain"),
    ("Sri Lanka","Sri Lanka"),
    ("Sudan","Sudan"),
    ("Suriname","Suriname"),
    ("Swaziland","Swaziland"),
    ("Sweden","Sweden"),
    ("Switzerland","Switzerland"),
    ("Syria","Syria"),
    ("Taiwan","Taiwan"),
    ("Tajikistan","Tajikistan"),
    ("Tanzania","Tanzania"),
    ("Thailand","Thailand"),
    ("Togo","Togo"),
    ("Tonga","Tonga"),
    ("Trinidad & Tobago","Trinidad & Tobago"),
    ("Tunisia","Tunisia"),
    ("Turkey","Turkey"),
    ("Turkmenistan","Turkmenistan"),
    ("Tuvalu","Tuvalu"),
    ("Uganda","Uganda"),
    ("Ukraine","Ukraine"),
    ("United Arab Emirates","United Arab Emirates"),
    ("United Kingdom","United Kingdom"),
    ("United States","United States"),
    ("Uruguay","Uruguay"),
    ("Uzbekistan","Uzbekistan"),
    ("Vanuatu","Vanuatu"),
    ("Vatican City","Vatican City"),
    ("Venezuela","Venezuela"),
    ("Vietnam","Vietnam"),
    ("Yemen","Yemen"),
    ("Zambia","Zambia"),

]


treatmentMethodsList=[('video_chat/skype', 'Video Chat/Skype'), ('phone', 'Phone'), ('in_person','In Person'), ('intensive_outpatient_settings', 'Intensive Outpatient')]


class LoginForm(Form):
    email    = StringField('Email', validators=[DataRequired()], description='enter your email')
    password = PasswordField('Password', validators=[DataRequired()], default='enter your password')
    date     = HiddenField('Date')
class TherapistRegistrationForm(Form):
    global stateChoices
    global countryChoices
    global treatmentMethodsList
    name             = StringField('Name', validators=[DataRequired()])
    email            = StringField('Email', validators=[DataRequired()])
    password         = PasswordField('Password', [InputRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword  = PasswordField('Confirm Password')
    nameOfPractice   = StringField('Name Of Practice', validators=[DataRequired()])
    treatmentMethods = SelectMultipleField('Treatment Methods', choices=treatmentMethodsList, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    address          = StringField('Address', validators=[DataRequired()])
    city             = StringField('City', validators=[DataRequired()])
    state            = SelectField('State', choices=stateChoices, validators=[DataRequired()])
    country          = SelectField('Country', choices=countryChoices, validators=[DataRequired()])



class ScheduleAppForm(Form) :
    dated        =StringField('Date:', validators=[DataRequired()])
    time        =StringField('Time:', validators=[DataRequired()], default="12:00 PM")
    userID      =StringField('userID:', validators=[DataRequired()])

class EnterNoteForm(Form) :
    noteID      =StringField('Note Title:', validators=[DataRequired()])
    note        =TextAreaField('Note', validators=[DataRequired()])

class editNoteForm(Form) :
    noteID      =StringField('Note Title:', validators=[DataRequired()])
    note        =TextAreaField('Note', validators=[DataRequired()])
    oldNoteID   =StringField('Note Title:', validators=[DataRequired()])

class InvitePatientForm(Form) :
    recipient   =StringField("Patient's Email:", validators=[DataRequired()])
    invitation  =TextAreaField('Invitation', validators=[DataRequired()])


class addERPHWForm (Form) :
    obsessions  =SelectField('OCD Theme', validators=[DataRequired()])
    triggers    =StringField('Trigger', validators=[DataRequired()])
    places      =StringField('Place', validators=[DataRequired()])
    time        =StringField('Time:', validators=[DataRequired()], default="12:00 PM")
    localtime   =StringField('localtime:', validators=[DataRequired()])
    prompt      =TextAreaField('Prompt')
