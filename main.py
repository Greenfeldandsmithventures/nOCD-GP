#import necessities from flask
from flask import Flask, request, render_template, session, Markup
#import form protection from flaskWTF 
from flask_wtf import Form, CsrfProtect
#import forms
from forms import LoginForm, TherapistRegistrationForm

#import entities for ndb datastore
from entities import Specialist, Manager, Patient


#general imports
import random
import string
import json



app = Flask(__name__) 
#Generate Random String to append to secretKey Base
temp=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
#set secret key for app
app.secret_key="pop_pop_pop_Ponoma_47!!!!_pow_pow_pow"
#Initialize csrf protection for application
CsrfProtect(app)
csrf=CsrfProtect()
#set Debug Mode True 
app.config['DEBUG'] = True


# We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

patient=Patient(name="John Bon", email="JohnBon@mail.com", uniqueID="1", id="1", nextAppointment="9/5/2015", episodes=12)
patient.put()
patient=Patient(name="Dohn Bon", email="DohnBon@mail.com", uniqueID="2", id="2", nextAppointment="9/9/2015", episodes=2)
patient.put()
patient=Patient(name="John Ban", email="JohnBan@mail.com", uniqueID="3", id="3", nextAppointment="9/7/2015", episodes=8)
patient.put()
patient=Patient(name="Stan the Man", email="StantheMan@mail.com", uniqueID="4", id="4", nextAppointment="9/8/2015", episodes=3)
patient.put()

specialist=Specialist.get_by_id('waterpolo234@gmail.com')
temp=['1','2','3','4']
specialist.patientCodes=json.dumps(temp)
specialist.put()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/therapistRegistration', methods=['GET','POST'])
def therapistRegistration():
    form=TherapistRegistrationForm()
    if request.method!='POST':
        return render_template('therapistRegistration.html', form=form)
    form=TherapistRegistrationForm(request.form)
    if form.password.data!=form.confirmPassword.data :
        return render_template('therapistRegistration.html', form=form, error="Uh Oh! Your passwords don't seem to match.")
    if form.validate():
        #check if the email is taken by testing if query returns null
        emailTaken=Specialist.get_by_id(form.email.data)
        if emailTaken :
            return render_template('therapistRegistration.html', form=form, error="Unfortunately that email seems to be in use already")
        #check if Practice name is taken
        practiceTaken=Specialist.query(Specialist.nameOfPractice==form.nameOfPractice.data)
        if practiceTaken.get() :
            return render_template('therapistRegistration.html', form=form, error="Unfortunately that Practice name seems to be in use already")
        #If at this point then email and Practice are unique so create new Specialist
        #To do this first create dict of types of practice
        typesOfPr=request.form.getlist('treatmentMethods')
        typesOfPr=json.dumps(typesOfPr)
        newSpecialist=Specialist(id=form.email.data, name=form.name.data, email=form.email.data, password=form.password.data, nameOfPractice=form.nameOfPractice.data, address=form.address.data, city=form.city.data,state=form.state.data, country=form.country.data, verified=False, emailVerified=False,  typesOfPractice=typesOfPr, patientCodes="[]")
        newSpecialist.put()
        return render_template('myPatients.html')
    return render_template('therapistRegistration.html', form=form, error="damn")
    


@app.route('/myPatients')
def myPatients() :
    patientRows=[]
    patientRowsAppointments=[]
    patientRowsName=[]
    patientRowsEpisodes=[]

    patients=[]
    patientsID=[]
    patientsName=[]
    patientsEpisodes=[]


    specialist=Specialist.get_by_id('waterpolo234@gmail.com')
    patientCodes=json.loads(specialist.patientCodes)
    for patientCode in patientCodes :
        patient=Patient.get_by_id(patientCode)
        patients.append(patient)


    patientsAppointments=sorted(patients, key=lambda patient: patient.nextAppointment)
    patientsName=sorted(patients, key=lambda patient: patient.name)
    patientsEpisodes=sorted(patients, key=lambda patient: patient.episodes)
    for patient in patients :
        tempRow='<tr>  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRows.append(Markup(tempRow))

    for patient in patientsAppointments :
        tempRow='<tr>  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRowsAppointments.append(Markup(tempRow))

    for patient in patientsName :
        tempRow='<tr>  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRowsName.append(Markup(tempRow))
    
    for patient in patientsEpisodes :
        tempRow='<tr>  <td class="nameColumn"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRowsEpisodes.append(Markup(tempRow))

    return render_template('myPatients.html', patientRows=patientRows,patientRowsAppointments=patientRowsAppointments, patientRowsName=patientRowsName, patientRowsEpisodes=patientRowsEpisodes)



@app.route('/login', methods=['POST']) 
def login():
    form=LoginForm()
    if request.method!='POST':
        return render_template('login.html', form=form)
    form=LoginForm(request.form)
    if request.method=='POST' and form.validate():
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)




#Handles new App User Information from Post
#Will contain special passcode from app
@csrf.exempt
@app.route('/registerAppUser', methods=['POST'])
def registerAppUser():
    if request.method!="POST" :
        return render_template('page_not_found.html')
    if request.form.secretConfirmationKey!="492968385622ijk!!@#$#llredereder" :
        return render_template('page_not_found.html')
    newPatient=Patient(name=request.form.name, password=request.form.password, email=request.form.email, uniqueID=request.form.uniqueID, id=request.form.uniqueID)
    newPatient.put()
    return "Success"



#Handles Posts By the Iphone App that Send User Data 
#Post will Include UserName and Password
#---These will be Used to grant access for storingData
#Return will be either Success or failure message 
@app.route('/depositUserData')
def depositUserData():
    pass

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@csrf.error_handler
def csrf_error(reason):
    return reason, 400