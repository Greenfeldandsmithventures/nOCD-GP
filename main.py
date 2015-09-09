#import necessities from flask
from flask import Flask, request, render_template, session, Markup
#import form protection from flaskWTF 
from flask_wtf import Form, CsrfProtect
#import forms
from forms import LoginForm, TherapistRegistrationForm
#import auxilliary functions
from auxillaryFunctions import sendEmail
#import entities for ndb datastore
from entities import Specialist, Manager, Patient, Obsession, Compulsion, Trigger


#general imports
import random
import string
import json


#temp=Obsession(id='1', obsessionID='1', userID='1', obsession="I forgot to lock the door")
#temp.put()
#temp=Obsession(id='2', obsessionID='2', userID='1', obsession="I forgot to turn off the stove")
#temp.put()
#temp=Obsession(id='3', obsessionID='3', userID='1', obsession="I forgot to lock the window")
#temp.put()
#temp=Obsession(id='4', obsessionID='4', userID='1', obsession="I forgot to turn off the lights")
#temp.put()

#temp=Trigger(id='1', obsessionID='1', userID='1', trigger="Leaving the kitchen" )
#temp.put()
#temp=Trigger(id='2', obsessionID='1', userID='1', trigger="Leaving the House" )
#temp.put()
#temp=Trigger(id='3', obsessionID='1', userID='1', trigger="Going to Bed" )
#temp.put()
#temp=Trigger(id='4', obsessionID='1', userID='1', trigger="Cooking" )
#temp.put()


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

#patient=Patient(name="John Bon", email="JohnBon@mail.com", uniqueID="1", id="1", nextAppointment="9/5/2015", episodes=12)
#patient.put()
#patient=Patient(name="Dohn Bon", email="DohnBon@mail.com", uniqueID="2", id="2", nextAppointment="9/9/2015", episodes=2)
#patient.put()
#patient=Patient(name="John Ban", email="JohnBan@mail.com", uniqueID="3", id="3", nextAppointment="9/7/2015", episodes=8)
#patient.put()
#patient=Patient(name="Stan the Man", email="StantheMan@mail.com", uniqueID="4", id="4", nextAppointment="9/8/2015", episodes=3)
#patient.put()

#specialist=Specialist.get_by_id('ecpraterfahey@gmail.com')
#temp=['1','2','3','4']
#specialist.patientCodes=json.dumps(temp)
#specialist.put()

#handle requests to home page
@app.route('/')
def home():
    return render_template('home.html')

#therapist registration
#Get--Returns Registration page
#Post--If successful sends verification email and returns 
#       veriryEmail page 
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
        secretCode=''.join(random.choice(string.ascii_uppercase) for _ in range(14)) 
        newSpecialist=Specialist(id=form.email.data, name=form.name.data, email=form.email.data, password=form.password.data, nameOfPractice=form.nameOfPractice.data, address=form.address.data, city=form.city.data,state=form.state.data, country=form.country.data, verified=False, emailVerified=False,  typesOfPractice=typesOfPr, patientCodes="[]", secretCode=secretCode)
        html='''
            <!DOCTYPE <html>
            <head>
            </head>

            <body>
                <p>Please follow the link bellow to complete your registration</p>
                <a href="nocdportal.appspot.com/verifyEmail?email='''+form.email.data+"&secretCode="+secretCode+'''">Verify Email</a>
            </body>
            </html>'''
        sender="nOCD@treatMyOCD.com"
        recipient=form.email.data
        subject="Verifying nOCD Email"
        emailSent=sendEmail(sender=sender, recipient=recipient, subject=subject,html=html,text="")
        if not emailSent :
            return render_template('therapistRegistration.html', form=form, error="Unfortunately there was an error please try registering again")
        newSpecialist.put()
        return render_template('verifyEmail.html')
    return render_template('therapistRegistration.html', form=form)
    

#Email verification
#Get--Successful returns emailVerified page
#     failure returns page not found
@app.route('/verifyEmail')
def emailVerification() :
    email=request.values.get('email')
    secretCode=request.values.get('secretCode')
    specialist=Specialist.get_by_id(email)
    if not specialist :
        return render_template('page_not_found.html')
    if specialist.secretCode!=secretCode :
        return render_template('page_not_found.html')
    specialist.emailVerified=True
    specialist.put()
    return render_template('emailVerified.html')        

#My patients page
#Get--Logged In--Returns myPatients page
#     not logged In returns Login Page 
@app.route('/myPatients')
def myPatients() :

    if not session.get('logged_in', False) :
        return Login()
    #load the specialists data
    specialist=Specialist.get_by_id(session['specialistID'])
    if not specialist.emailVerified :
        return render_template('verifyEmail.html')
    #Lists to store the <tr> rows for each sorted list
    patientRowsAppointments=[]
    patientRowsName=[]
    patientRowsEpisodes=[]

    #lists to store the patients data in order
    patients=[]
    patientsID=[]
    patientsName=[]
    patientsEpisodes=[]

    #load specialists patientCodes
    patientCodes=json.loads(specialist.patientCodes)

    #load each patients data
    for patientCode in patientCodes :
        session[patientCode]=True
        patient=Patient.get_by_id(patientCode)
        patients.append(patient)

    #sort patients into each seperate sorted list
    patientsAppointments=sorted(patients, key=lambda patient: patient.nextAppointment)
    patientsName=sorted(patients, key=lambda patient: patient.name)
    patientsEpisodes=sorted(patients, key=lambda patient: patient.episodes)

    #create <tr> rows for each table
    for patient in patientsAppointments :
        tempRow='<tr onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRowsAppointments.append(Markup(tempRow))

    for patient in patientsName :
        tempRow='<tr onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRowsName.append(Markup(tempRow))
    
    for patient in patientsEpisodes :
        tempRow='<tr onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        tempRow=tempRow+patient.nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(patient.episodes)+"</td> </tr>"
        patientRowsEpisodes.append(Markup(tempRow))

    return render_template('myPatients.html',patientRowsAppointments=patientRowsAppointments, patientRowsName=patientRowsName, patientRowsEpisodes=patientRowsEpisodes)

@app.route('/myPatients/<patientCode>')
def viewPatient(patientCode) :
    #verify logged in 
    if not session.get(patientCode, False) :
        return render_template('page_not_found.html')
    #Load patient data
    patient=Patient.get_by_id(patientCode)
    
    #verify patient Found
    if not patient :
        return render_template('page_not_found.html')
    obsessions=Obsession.query(Obsession.userID==patientCode)
    obsessionPills=[]
    obsessionPanes=[]
    for obsession in obsessions :
        row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+obsession.obsessionID+'">'
        row+=obsession.obsession+'</a></li>'
        obsessionPills.append(Markup(row))
        #add obsessionPanes
        row='<div id="'+obsession.obsessionID+'" class="tab-pane fade in">'
        row+='<div class="row"><div class="col-xs-6"><h4 align="center">Triggers</h4>'
        triggers=Trigger.query(Trigger.obsessionID==obsession.obsessionID)
        for trigger in triggers :
            row+='<h6>'+trigger.trigger+'</h6>'
        row+='</div> <div class="col-xs-6"><h4 align="center">Compulsions</h4>'
        compulsions=Compulsion.query(Compulsion.obsessionID==obsession.obsessionID)
        for compulsion in compulsions :
            row+='<h6>'+compulsion.compulsion+'</h6>'
        row+='</div></div></div>'
        obsessionPanes.append(Markup(row))
    return render_template('patientPage.html', patient=patient, obsessionPills=obsessionPills, obsessionPanes=obsessionPanes)


@app.route('/login', methods=['GET','POST']) 
def login():
    if session.get('logged_in',False) :
        return myPatients()
    form=LoginForm()
    if request.method!='POST':
        return render_template('login.html', form=form)
    form=LoginForm(request.form)
    if request.method=='POST' and form.validate():
        specialist=Specialist.get_by_id(form.email.data)
        if not specialist :
            return render_template('login.html', form=form, error="Email not found")
        if specialist.password!=form.password.data :
            return render_template('login.html', form=form, error="Incorrect password")
        if not specialist.emailVerified :
            return render_template('verifyEmail.html')
        session['logged_in']=True
        session['specialistID']=form.email.data
        return myPatients()
    return render_template('login.html', form=form)

@app.route('/logout')
def logout() :
    session.clear()
    return home()


#Handles new App User Information from Post
#Will contain special passcode from app
@csrf.exempt
@app.route('/registerAppUser', methods=['POST'])
def registerAppUser():
    if request.method!="POST" :
        return render_template('page_not_found.html')
    if request.form.secretConfirmationKey!="yywrt4929683reghalkd85622ijk!!@#$#llredereder" :
        return render_template('page_not_found.html')
    newPatient=Patient(name=request.form.name, password=request.form.password, email=request.form.email, uniqueID=request.form.uniqueID, id=request.form.uniqueID)
    newPatient.put()
    return "Success"


@csrf.exempt
@app.route('/requestToTherapist')
def requestToTherapist():
    if request.method!="POST" :
        return render_template('page_not_found.html')
    if request.form.secretConfirmationKey!="yywrt4929683reghalkd85622ijk!!@#$#llredereder" :
        return render_template('page_not_found.html')
    specialist=Specialist.get_by_id(request.form.specialistID)
    patientRequests=json.loads(specialist.patientRequests)
    newRequest={}
    newRequest.name=request.form.name
    newRequest.patientID=request.form.patientID
    newRequest.password=request.form.password
 
@app.errorhandler
def pop(error) :
    return error

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@csrf.error_handler
def csrf_error(reason):
    return reason, 400