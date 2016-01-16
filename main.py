#import necessities from flask
from flask import Flask, request, render_template, session, Markup, Response
#import form protection from flaskWTF 
from flask_wtf import Form, CsrfProtect
#import forms
from forms import LoginForm, TherapistRegistrationForm, EnterNoteForm, addERPHWForm, editNoteForm, InvitePatientForm,ScheduleAppForm
#import auxilliary functions
from auxillaryFunctions import sendEmail, generateCalendar, ERPGraphs, EpisodeGraphs, Hasher, Unhash, generateCalendars
#import entities for ndb datastore
from entities import Specialist, Manager, Patient, Obsession, Compulsion, Trigger, Note, ERPHW, Place, Request, Episode, Errorr
#import ndb
from google.appengine.ext import ndb
#imports for posting
from google.appengine.api import urlfetch
import urllib


#general imports
import random, datetime, time,calendar
import string
import json

#specs=Specialist.query()

#for spec in specs :
#    spec.numberRequests=0
#    spec.put()


rep=Request(patientName=Hasher("Test Account T"), userID=Hasher("129"), specialistID="ecpraterfahey@gmail.com", message=None)
rep.put()
#variables
secretKey="ywrt492y9683reghalkd85622ijkllrex58wwsqquidnj"
#the variable for url for posting new ERP HW
urlForERPAdd="http://104.196.18.200/nocd/index.php/api/add_scheduled_erp"
#the variable for url for getting user Info
urlForUserInfo="http://104.196.18.200/nocd/index.php/api/get_user_info"
# the variable for removing erpHW
urlForERPRemove="http://104.196.18.200/nocd/index.php/api/delete_scheduled_erp"
#temp=Obsession(id='1', obsessionID='1', userID='1', obsession="What if I forgot to lock the door")
#temp.put()
#temp=Obsession(id='2', obsessionID='2', userID='1', obsession="What if I forgot to turn off the stove")
#temp.put()
#temp=Obsession(id='3', obsessionID='3', userID='1', obsession="What if I forgot to lock the window")
#temp.put()
#temp=Obsession(id='4', obsessionID='4', userID='1', obsession="What if I forgot to turn off the lights")
#temp.put()

#temp=Place(placeID="1", userID='1', place="My kitchen")
#temp.put()
#temp=Trigger(id='1', triggerID='1', obsessionID='2', userID='1', trigger="Leaving the kitchen" )
#temp.put()
#temp=Trigger(id='2', triggerID='2', obsessionID='2', userID='1', trigger="Leaving the House" )
#temp.put()
#temp=Trigger(id='3', triggerID='3', obsessionID='2', userID='1', trigger="Going to Bed" )
#temp.put()
#temp=Trigger(id='4', triggerID='4', obsessionID='2', userID='1', trigger="Cooking" )
#temp.put() 


app = Flask(__name__) 
#Generate Random String to append to secretKey Base
temp=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
#set secret key for app
app.secret_key="pop_pop_pop_Ponoma_47!!!!_pow_pow_pow"
#Initialize csrf protection for application
#CsrfProtect(app)
csrf=CsrfProtect(app)
#set Debug Mode True 
app.config['DEBUG'] = True


# We don't need to call run() since our application is embedded within
 # the App Engine WSGI application server.

patient=Patient(name=Hasher("Test Account T"),firstName=Hasher("Test"), email=Hasher("e11ere8@gmail.com"), uniqueID=Hasher("129"), id=Hasher("129"), nextAppointment=None, episodes=None)
patient.put()
#patient=Patient(name=Hasher("Caleb Prater"), email=Hasher("e1108@gmail.com"), uniqueID=Hasher("36"), id=Hasher("36"), nextAppointment=None, episodes=None)
#patient.put()
#patient=Patient(firstName="Dohn", name="Dohn Bon", email="DohnBon@mail.com", uniqueID="2", id="2", nextAppointment="9/9/2015", episodes=2)
#patient.put()
#patient=Patient(firstName="John", name="John Ban", email="JohnBan@mail.com", uniqueID="3", id="3", nextAppointment="9/7/2015", episodes=8)
#patient.put()
#patient=Patient(firstName="Stan", name="Stan the Man", email="StantheMan@mail.com", uniqueID="4", id="4", nextAppointment="9/8/2015", episodes=3)
#patient.put()

#trigger=Trigger(triggerID="5", obsessionID='1', trigger="Going to Work", userID="1")
#trigger.put()
#trigger=Trigger(triggerID="6", obsessionID='1', trigger="Leaving the living room", userID="1")
#trigger.put()

#place=Place(placeID="1", userID="1", place="My living room", obsessionID="1")
#place.put()
#place=Place(placeID="2", userID="1", place="In front of my house", obsessionID="1")
#place.put()#

#trigger=Trigger(triggerID="7", obsessionID='4', trigger="Going to Work", userID="1")
#trigger.put()
#trigger=Trigger(triggerID="8", obsessionID='4', trigger="Leaving the living room", userID="1")
#trigger.put() 

#place=Place(placeID="3", userID="1", place="My living room", obsessionID="4")
#place.put()
#place=Place(placeID="4", userID="1", place="In front of my house", obsessionID="4")
#place.put() 3



#trigger=Trigger(triggerID="5", obsessionID='1', trigger="Going to Work", userID="1")
#trigger.put()
#specialist=Specialist.get_by_id('ecpraterfahey@gmail.com')
#specialist.password=Hasher(specialist.password)
#temp=[]
#specialist.patientCodes=json.dumps(temp)
#specialist.verified=True
#specialist.put() 

#handle requests to home page
@app.route('/')
def home():
    return render_template('home.html')

@csrf.exempt
@app.route('/verifyTherapist/<therapistEmail>', methods=['GET','POST'])
def verifyTherapist(therapistEmail):
    if request.method!='POST':
        return "Innapropriate Request"
    if request.form['secretCode'] != "ThisistheSecretCode426374834445453233jrjr" :
        return "OOps Wrong Code"
    specialist=Specialist.get_by_id(therapistEmail)
    specialist.verified=True
    specialist.put()
    sender='noresponse@nocdinfo.com'
    recipient=therapistEmail
    subject='nOCD Specialist Account Verified'
    text="We are pleased to inform you that your Specialist account with nOCD has been verified. You can now use all of the functions on the portal at https://nocdportal.appspot.com/"
    emailSent=sendEmail(sender=sender, recipient=recipient, subject=subject,html="",text=text)
    return "Success"



#handle requests to home page 2.o
@app.route('/home')
def home2():
    return render_template('home2.html')


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
        newSpecialist=Specialist(id=form.email.data, name=form.name.data, email=form.email.data, password=Hasher(form.password.data), nameOfPractice=form.nameOfPractice.data, address=form.address.data, city=form.city.data,state=form.state.data, country=form.country.data, verified=False, emailVerified=False,  typesOfPractice=typesOfPr, patientCodes="[]", secretCode=secretCode)
        theText="If the link does not work you can copy and paste this url into your browser https://nocdportal.appspot.com/verifyEmail?email="+form.email.data+"&secretCode="+secretCode

        html='''
            <!DOCTYPE <html>
            <head>
            </head>

            <body>
                <p>Please follow the link bellow to complete your registration</p>
                <a href="nocdportal.appspot.com/verifyEmail?email='''+form.email.data+"&secretCode="+secretCode+'''">Verify Email</a>
                
                <p>If the link does not work you can copy and paste this url into your browser https://nocdportal.appspot.com/verifyEmail?email='''+form.email.data+"&secretCode="+secretCode+''' </p>

            </body>
            </html>'''
        sender="nOCD@treatMyOCD.com"
        recipient=form.email.data
        subject="Verifying nOCD Email"
        emailSent=sendEmail(sender=sender, recipient=recipient, subject=subject,html=html,text=theText)
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
        return login()
    #load the specialists data
    specialist=Specialist.get_by_id(session['specialistID'])
    if not specialist.emailVerified :
        return render_template('verifyEmail.html')
    #Lists to store the <tr> rows for each sorted list
    patientRowsAppointments=[]
    patientRowsName=[]
    patientRowsEpisodes=[]
    patientRowsAppointmentsDe=[]
    patientRowsNameDe=[]
    patientRowsEpisodesDe=[]

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
        lastApp=None
        try :
            lastApp=patient.lastAppointment
        except :
            patient.lastAppointment="12-11-10 01:00PM"
        #numEpisodes=0
        #episodes=Episode.query(Episode.userID==patientCode)
        #for episode in episodes :
        #    if episode.dateTime[:10] >patient.lastAppointment :
        #        numEpisodes+=1
        #patient.episodes=numEpisodes
        patient.name=Unhash(patient.name)
        patients.append(patient)
        #patient.put()




    #sort patients into each seperate sorted list
    patientsAppointments=sorted(patients, key=lambda patient: patient.nextAppointment)
    patientsName=sorted(patients, key=lambda patient: patient.name)
    patientsEpisodes=sorted(patients, key=lambda patient: patient.episodes)

    #create <tr> rows for each table

    for patient in patientsAppointments :
        tempRow='<tr class="handy" onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        nextAppointment=""
        if patient.nextAppointment :
            nextAppointment=patient.nextAppointment
        numEpisodes=0
        if patient.episodes :
            numEpisodes=patient.episodes

        tempRow=tempRow+nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(numEpisodes)+"</td> </tr>"
        patientRowsAppointments.append(Markup(tempRow))

    for patient in patientsName :
        tempRow='<tr class="handy" onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        nextAppointment=""
        if patient.nextAppointment :
            nextAppointment=patient.nextAppointment
        numEpisodes=0
        if patient.episodes :
            numEpisodes=patient.episodes

        tempRow=tempRow+nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(numEpisodes)+"</td> </tr>"
        patientRowsName.append(Markup(tempRow))
    

    for patient in patientsEpisodes :
        tempRow='<tr class="handy" onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        nextAppointment=""
        if patient.nextAppointment :
            nextAppointment=patient.nextAppointment
        numEpisodes=0
        if patient.episodes :
            numEpisodes=patient.episodes

        tempRow=tempRow+nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(numEpisodes)+"</td> </tr>"
        patientRowsEpisodes.append(Markup(tempRow))



    patientsAppointments.reverse()
    patientsName.reverse()
    patientsEpisodes.reverse()

 

    for patient in patientsAppointments :
        tempRow='<tr class="handy" onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        nextAppointment=""
        if patient.nextAppointment :
            nextAppointment=patient.nextAppointment
        numEpisodes=0
        if patient.episodes :
            numEpisodes=patient.episodes

        tempRow=tempRow+nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(numEpisodes)+"</td> </tr>"
        patientRowsAppointmentsDe.append(Markup(tempRow))

    for patient in patientsName :
        tempRow='<tr class="handy" onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn activo"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        nextAppointment=""
        if patient.nextAppointment :
            nextAppointment=patient.nextAppointment
        numEpisodes=0
        if patient.episodes :
            numEpisodes=patient.episodes

        tempRow=tempRow+nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(numEpisodes)+"</td> </tr>"
        patientRowsNameDe.append(Markup(tempRow))
    

    for patient in patientsEpisodes :
        tempRow='<tr class="handy" onclick="location.href=\'/myPatients/'+patient.uniqueID+'\';">  <td class="nameColumn"> <span class="glyphicon glyphicon-user blue"></span>'        
        tempRow=tempRow+patient.name+'</td> <td class="appointmentColumn">'
        nextAppointment=""
        if patient.nextAppointment :
            nextAppointment=patient.nextAppointment
        numEpisodes=0
        if patient.episodes :
            numEpisodes=patient.episodes

        tempRow=tempRow+nextAppointment+'</td> <td class="episodeColumn">'
        tempRow=tempRow+str(numEpisodes)+"</td> </tr>"
        patientRowsEpisodesDe.append(Markup(tempRow))



    return render_template('myPatients.html',numRequests=specialist.numberRequests,
                                             patientRowsAppointments=patientRowsAppointments, 
                                             patientRowsName=patientRowsName, 
                                             patientRowsEpisodes=patientRowsEpisodes,
                                             patientRowsAppointmentsDe=patientRowsAppointmentsDe, 
                                             patientRowsNameDe=patientRowsNameDe, 
                                             patientRowsEpisodesDe=patientRowsEpisodesDe)

 
#remove Patient
@app.route('/removePatient/<userID>') 
def removePatient(userID) :
    user=Patient.get_by_id(userID)
    newRequest=Request(specialistID=session['specialistEmail'], patientName=user.name, userID=userID)
    newRequest.put()
    specialist=Specialist.get_by_id(session['specialistID'])
    codes=json.loads(specialist.patientCodes) 
    codes.remove(userID)
    specialist.patientCodes=json.dumps(codes)
    specialist.numberRequests+=1
    session['numRequests']+=1
    specialist.put()
    return myPatients()


#View patient 
@app.route('/viewRequests') 
def viewRequests() :
    #verify logged in 
    if not session.get('logged_in', False) :
        return render_template('page_not_found.html')
    if not session['verified'] :
        return render_template('beingVerified.html', numRequests=session['numRequests'])
    requests=Request.query(Request.specialistID==session['specialistID'])

    requestPills=[]
    requestPanes=[]
    isFirst=True
    requestsPresent=False
    table=""
    for requester in requests :
        requester.patientName=Unhash(requester.patientName)
        requestsPresent =True
        table+="<tr><td>"+requester.patientName+"</td><td><a class='btn btn-success' href='/registerPatient/"+str(requester.key.id())+"'>Accept</a></td><td><a class='btn btn-danger' href='/denyPatient/"+str(requester.key.id())+"'>Reject</a></td></tr>"

        row=""
        if isFirst :
            row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+requester.patientName+'">'
        else :
            row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+requester.patientName+'">'

        row+=requester.patientName+'</a></li>'
        requestPills.append(Markup(row))

        row=""
        if isFirst :
            row='<div id="'+requester.patientName+'" class="tab-pane fade in active">'
            isFirst=False
        else :
            row='<div id="'+requester.patientName+'" class="tab-pane fade in">'
        #row+=requester.message
        requestPanes.append(Markup(row))

    return render_template('viewRequests.html', numRequests=session['numRequests'], theTable=Markup(table),requestsPresent=requestsPresent, requestPills=requestPills, requestPanes=requestPanes)


#Invite patient via email
@app.route('/invitePatient', methods=["GET", "POST"]) 
def invitePatient() :
    #verify logged in 
    if not session.get('logged_in', False) :
        return render_template('page_not_found.html')
    if not session['verified'] :
        return render_template('beingVerified.html', numRequests=session['numRequests'])
    if request.method != "POST" :
        form=InvitePatientForm()
        return render_template('invitePatient.html',numRequests=session['numRequests'], form=form, error=None, successs=None,hideDanger="hidden")
    form=InvitePatientForm(request.form)
    if not form.validate() :
        return render_template('invitePatient.html', numRequests=session['numRequests'],form=form, error="Uh Oh looks like something went wrong", successs=None,hideDanger="")
    html=form.invitation.data
    sender=session['specialistEmail']
    recipient=form.recipient.data
    subject="Using the 'nOCD' App for Treatment"
    emailSent=sendEmail(sender=sender, recipient=recipient, subject=subject,html=html,text="")
    if not emailSent :
        return render_template('invitePatient.html', numRequests=session['numRequests'],form=form, error="Oops looks like something went wrong", successs=None,hideDanger="")
    form=InvitePatientForm()
    return render_template('invitePatient.html', numRequests=session['numRequests'],form=form, error=None, success="Success",hideDanger="hidden")

#Individual Patients Loading page
@app.route('/myPatients/<patientCode>')
def viewPatient(patientCode) :
    return render_template('loading.html', numRequests=session['numRequests'],patientCode=patientCode)

#Individual Patients page
@app.route('/myPatients/patient/<patientCode>')
def viewPatients(patientCode) :
    #verify logged in  
    if not session.get(patientCode, False) :
        return render_template('page_not_found.html')
    #Load patient data
    patient=Patient.get_by_id(patientCode)
    #verify patient Found
    if not patient :
        return render_template('page_not_found.html')
    session['userID']=patientCode
    patient.name=Unhash(patient.name)
    patient.email=Unhash(patient.email)
    patient.firstName=patient.name.split(" ")[0]
    form_fields = {
        "userID": Unhash(patientCode)
    }
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url=urlForUserInfo,
    payload=form_data,
    method=urlfetch.POST,
    headers={'Content-Type': 'application/x-www-form-urlencoded'})

    results=json.loads(result.content)
    content=results['info']
    #return json.dumps(content)

    #load users obsessions
    obsessions=[]
    obs={}
    theObsessions=content.get('obsessions', False)
    if theObsessions :
        for obsession in theObsessions :
            newObsession=Obsession(id=obsession['obsessionID'], obsessionID=obsession['obsessionID'], userID=patientCode, obsession=obsession['obsession'])
            obs[obsession['obsessionID']]=newObsession
            obsessions.append(newObsession)
            #newObsession.put()
    #load users Triggers
    triggers={}
    trigs={}
    theTriggers=content.get('triggers', False)
    if theTriggers :
        for trigger in theTriggers :
            newTrigger=Trigger(id=trigger['triggerID'], triggerID=trigger['triggerID'], obsessionID=trigger['obsessionID'], userID=patientCode, trigger=trigger['trigger'])
            trigs[trigger['triggerID']]=newTrigger
            if triggers.get(newTrigger.obsessionID, False) :
                triggers[newTrigger.obsessionID].append(newTrigger)
            else :
                triggers[newTrigger.obsessionID]=[newTrigger]
            #newTrigger.put()
    else :
        pass
    #load users Compulsions
    compulsions={}
    comps={}
    theCompulsions=content.get('compulsions', False)
    if theCompulsions :
        for compulsion in theCompulsions :
            newCompulsion=Compulsion(id=compulsion['compulsionID'], obsessionID=compulsion['obsessionID'], compulsionID=compulsion['compulsionID'], userID=patientCode, compulsion=compulsion['compulsion'])
            comps[compulsion['compulsionID']]=newCompulsion
            if compulsions.get(newCompulsion.obsessionID, False) :
                compulsions[newCompulsion.obsessionID].append(newCompulsion)
            else :
                compulsions[newCompulsion.obsessionID]=[newCompulsion]
            #newCompulsion.put()
             
    #load users Places
    places={}
    thePlaces=content.get('places', False)
    if thePlaces :
        for place in thePlaces :
            newPlace=Place(id=place['id'], placeID=place['id'], userID=patientCode, place=place['locationAddress'], latitude=place['lat'], longitude=place['lng'])
            #newPlace.put()
            if places.get(newPlace.obsessionID, False) :
                places[newPlace.obsessionID].append(newPlace)
            else :
                places[newPlace.obsessionID]=[newPlace]
    # load users erp hws 
    #return "Made it through Loading in all Obsessions Compulsions triggers and places"
    erpHWs=[]
    erps=content.get('scheduled_erp', False) 
    if erps :
        for erp in erps :
            status="Incomplete"
            if erp['done']=='1' :
                status="Complete"
            militTime=erp['scheduledDate'][-8:-3]
            hours=militTime[:2]
            minutes=militTime[3:]
            time=""
            timing="AM"
            if int(hours)>=12 :
                timing="PM"
            if int(hours) >12 :
                time=str(int(hours)-12)
            else :
                time=hours
            if int(hours)==24 :
                timing="AM"
            time=time+":"+minutes+timing
            newERP=ERPHW(id=erp['scheduledID'], intensity=erp['anxiety'], HWID=erp['scheduledID'], userID=patientCode, status=status, obsession=erp['obssesion'], obsessionID=erp['obsessionID'], trigger=erp['trigger'], triggerID=erp['triggerID'], place=erp['place'], prompt="", resistanceTime=erp['spentTime'].split(".")[0], time=time, dateTime=erp['scheduledDate'], new=False)
            erpHWs.append(newERP)
            #newERP.put()

    # load users episodes 
    episodes=[]
    theEpisodes=content.get('episodes', False) 
    if theEpisodes :
        for ep in theEpisodes :
            militTime=ep['epsDate'][-8:-3]
            hours=militTime[:2]
            minutes=militTime[3:]
            time=""
            timing="AM"
            if int(hours)>=12 :
                timing="PM"
            if int(hours) >12 :
                time=str(int(hours)-12)
            else :
                time=hours
            if int(hours)==24 :
                timing="AM"
            time=time+":"+minutes+timing
            trigger=None
            if ep['triggerID']!='0' :
                try :
                    trigger=trigs[ep['triggerID']].trigger
                except :
                    pass
            obsession=None
            if ep['obsessionID']!='0' :
                obsession=obs[ep['obsessionID']].obsession
            compulsion=None
            #if ep['compulsionID']!='0' :    #when including this if statement getting error becuase compulsion doesnt seem to exist?
            #    compulsion=comps[ep['compulsionID']].compulsion

            newep=Episode(id=ep['epsId'], episodeID=ep['epsId'], userID=patientCode, obsessionID=ep['obsessionID'], resistanceTime=ep['compulsionTime'].split(".")[0], obsession=obsession, trigger=trigger, triggerID=ep['triggerID'], place=ep['locationAddress'], heartRate=int(ep['heartRate']) , intensity=int(ep['intense']), time=time, dateTime=ep['epsDate'], latitude=float(ep['lat']), longitude=float(ep['lng']))
            episodes.append(newep)
            #newep.put()
    else :
        pass


    #return "Made it through Loading in all data"
    #obsessions=Obsession.query(Obsession.userID==patientCode)
    obsessionPills=[]
    obsessionPanes=[]

    triggerList={}
    obsessionList=[]
    placeList={}

    isFirst=True
    #generate obsessions tabs containing associated triggers and Compulsions
    for obsession in obsessions :
        obsessionList.append((obsession.obsessionID,obsession.obsession.replace('"',"&quot;").replace("'","&#39;")))
        
        #adding to obsessionpills
        #
        if isFirst :
            row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+obsession.obsessionID+'">'
        else :
            row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+obsession.obsessionID+'">'
        row+=obsession.obsession+'</a></li>'
        obsessionPills.append(Markup(row))
        
        #adding to obsessionPanes
        #
        if isFirst :
            row='<div id="'+obsession.obsessionID+'" class="tab-pane fade in active">'
            isFirst=False
        else :
            row='<div id="'+obsession.obsessionID+'" class="tab-pane fade in">'
        #adding triggers to obsessionpane
        row+='<div class="row"><div class="col-xs-6"><h4 align="center">Triggers</h4>'
        #triggers=Trigger.query(Trigger.obsessionID==obsession.obsessionID)
        newTriggerList=[]
        if triggers.get(obsession.obsessionID, False) :
            for trigger in triggers[obsession.obsessionID] :
                newTriggerList.append((trigger.triggerID,trigger.trigger.replace('"',"&quot;").replace("'","&#39;")))
                row+='<h6>'+trigger.trigger+'</h6>'
        triggerList[obsession.obsessionID.replace('"',"&quot;").replace("'","&#39;")]=newTriggerList
        row+='</div>'
        #adding places to obsessionpane
        #places=Place.query(Place.obsessionID==obsession.obsessionID)
        newPlaceList=[]
        if places.get(obsession.obsessionID, False) :
            for place in places :
                newPlaceList.append((place.placeID, place.place.replace('"',"&quot;").replace("'","&#39;")))
        placeList[obsession.obsessionID.replace('"',"&quot;").replace("'","&#39;")]=newPlaceList
        #adding compulsions to obsesion pane
        row+=' <div class="col-xs-6"><h4 align="center">Compulsions</h4>'
        #compulsions=Compulsion.query(Compulsion.obsessionID==obsession.obsessionID)
        if compulsions.get(obsession.obsessionID, False) :
            for compulsion in compulsions[obsession.obsessionID] :
                row+='<h6>'+compulsion.compulsion+'</h6>'
        row+='</div></div></div>'
        obsessionPanes.append(Markup(row))
    

    noteForm=EnterNoteForm()
    #generate note pills and panes
    notes=Note.query(Note.userID==patientCode, Note.specialistID==session['specialistID'])
    notePills=[]
    notePanes=[]
    noteNum=0
    for note in notes :
        if isFirst :
            row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+note.noteID.replace('#','aHashTag').replace(' ', '_')+'">'
        else :
            row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+note.noteID.replace('#','aHashTag').replace(' ', '_')+'">'
        row+=note.noteID+'</a></li>'
        notePills.append(Markup(row))
        tempID=note.noteID.replace('#','aHashTag').replace(' ', '_')
        if isFirst :
            row='<div id="'+tempID+'" class="tab-pane fade in active note-pane"> <center>'
            isFirst=False
        else :
            row='<div id="'+tempID+'" class="tab-pane fade in note-pane"> <center>'
        
        tempNote=editNoteForm()
        tempNote.noteID.data=note.noteID
        tempNote.oldNoteID.data=note.noteID
        row+=render_template('editNoteForm.html', noteForm=tempNote, note=Markup(note.note), noteNum=noteNum)
        noteNum+=1
        row+='</center></div>'


        notePanes.append(Markup(row))



    #generate note list for patient
    noteTitles=[]


    #notes=Note.query(Note.userID==patientCode, Note.specialistID==session['specialistID'])
    for note in notes :
        noteTitles.append(note.noteID)
    currMonth=session['theDate'].month

    #places=Place.query(Place.userID==patientCode)

    #for place in places :
    #    placeList.append((place.placeID, place.place))
    erpHWList=[]
    erpHWDict={}
    #erpHWs=ERPHW.query(ERPHW.userID==patientCode)
    hwByObsessionList="[['Obsession', 'Number'],"
    hws={}
    trggrs={}
    hwsByMonth={}
    hwPills=""
    hwPanes=""
    isFirst=True
    # list for frequencies by month and week and year
    frequencies={}
    erpHWsSorted=sorted(erpHWs, key=(lambda g : g.dateTime))
    erpHWsSorted.reverse()
    for erpHW in erpHWsSorted :
        erpDate=None
        proceed=True
        try :
            erpDate=datetime.datetime.strptime(erpHW.dateTime[:10], '%Y-%m-%d')
        except :
            proceed=False
        if proceed :
            #add to hwPills 
            hwID=erpHW.HWID.replace('/','slashed').replace(' ','spacing').replace(':','colon').replace('-','dash')
            if isFirst :
                row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+hwID+'">'
            else :
                row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+hwID+'">'
            row+=erpHW.dateTime[:10]+'</a></li>'
            hwPills+=row

            if frequencies.get(str(erpDate.year), False) :
                if frequencies[str(erpDate.year)].get(str(erpDate.isocalendar()[1]), False) :
                    if frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])].get(str(erpDate.isocalendar()[2]), False) :
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']+=['p']
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']+=1
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']+=1
                        frequencies[str(erpDate.year)]['number']+=1
                    else :
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']=['p']
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                        frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']+=1
                        frequencies[str(erpDate.year)]['number']+=1
                else :
                    frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]={}
                    frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                    frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']=['p']
                    frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                    frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']=1
                    frequencies[str(erpDate.year)]['number']+=1

            else :
                frequencies[str(erpDate.year)]={}
                frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]={}
                frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']=['p']
                frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                frequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']=1
                frequencies[str(erpDate.year)]['number']=1


            if isFirst :
                row='<div id="'+hwID+'" class="tab-pane fade in active">'
                isFirst=False
            else :
                row='<div id="'+hwID+'" class="tab-pane fade in">'

            anxietyLevel="No Data"
            if erpHW.intensity!="" :
                anxietyLevel=erpHW.intensity
            place="No Data"
            if erpHW.place!="" :
                place=erpHW.place
            timeSpent=""
            if (int(erpHW.resistanceTime) )/60 >=1:
                timeSpent=str(int(erpHW.resistanceTime)/60)+" minutes "+str(int(erpHW.resistanceTime) % 60)+" seconds"
            else :
                timeSpent=str(erpHW.resistanceTime)+" Seconds"

            row+='<table class="table table-bordered table-striped">'
            row+='<th colspan=\'2\' style=\'text-align:center !important\'>HW Summary </th>'
            row+='<tr><td><strong>Date</strong>:</td><td><strong>Time</strong>:</td></tr>'
            row+='<tr><td class="smaller">'+erpHW.dateTime[:10]+'</td><td class="smaller">'+erpHW.time+'</td></tr>'
            row+='<tr><td><strong>Obsession</strong>:</div><td><strong>Trigger</strong>:</div></tr>'
            row+='<tr><td class="smaller">'+erpHW.obsession+'</td><td class="smaller">'+erpHW.trigger+'</td></tr>'
            row+='<tr><td><strong>Status</strong>:</div><td><strong>Anxiety Level</strong>:</div></tr>'
            row+='<tr><td class="smaller">'+erpHW.status+'</td><td class="smaller">'+anxietyLevel+'</td></tr>'  
            row+='<tr><td><strong>Time Spent</strong>:</div><td><strong>Place</strong>:</div></tr>'
            row+='<tr><td class="smaller">'+timeSpent+'</td><td class="smaller">'+place+'</td></tr>' 
            row+='</table>'

            #row+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Prompt</strong>:</div></div>'
            #row+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><div contenteditable=\'true\'>'+erpHW.prompt.replace('"',"'")+'</div></div></div>'
            hwPanes+=row+"</div>"
            erpTemp={}
            temp=hws.get(erpHW.obsession, False)
            if temp :
                hws[erpHW.obsession]=[hws[erpHW.obsession][0],hws[erpHW.obsession][1]+1]
            else :
                hws[erpHW.obsession]=[erpHW.obsession,1]
            
            temp=trggrs.get(erpHW.trigger, False)
            if temp :
                trggrs[erpHW.trigger]=[trggrs[erpHW.trigger][0],trggrs[erpHW.trigger][1]+1]
            else :
                trggrs[erpHW.trigger]=[erpHW.trigger,1]
            hwWeekDate=datetime.datetime.strptime(erpHW.dateTime[:10], '%Y-%m-%d').date()
            temp=hwsByMonth.get(hwWeekDate.month, False)
            if temp :
                hwsByMonth[hwWeekDate.month]=[hwsByMonth[hwWeekDate.month][0],hwsByMonth[hwWeekDate.month][1]+1]
            else :
                hwsByMonth[hwWeekDate.month]=[hwWeekDate.month,1]
            erpTemp['HWID']=erpHW.HWID
            erpTemp['userID']=erpHW.userID
            if erpDate.date()<session['theDate'].date() :
                if erpHW.status!="Complete" :
                    erpHW.status="Missed"
                    #erpHW.put()

            erpTemp['status']=erpHW.status
            erpTemp['obsession']=erpHW.obsession
            if erpHW.obsession :
                erpTemp['obsession']=erpHW.obsession.replace('"',"&quot;").replace("'","&#39;")
            erpTemp['trigger']=erpHW.trigger
            if erpHW.trigger :
                erpTemp['trigger']=erpHW.trigger.replace('"',"&quot;").replace("'","&#39;")
            erpTemp['place']=erpHW.place
            erpTemp['prompt']=erpHW.prompt
            erpTemp['time']=erpHW.time
            erpTemp['dateTime']=erpHW.dateTime
            erpTemp['intensity']=erpHW.intensity
            erpTemp['place']=erpHW.place
            erpTemp['resistanceTime']=erpHW.resistanceTime

            if erpHWDict.get(erpDate.date(), False) :
                erpHWDict[erpDate.date()].append(erpTemp)
            else :
                erpHWDict[erpDate.date()]=[erpTemp]
            erpHWList.append(erpTemp)
    #return "about to generate calendar"
    #monthCalendars=generateCalendars(erpHWs=erpHWDict, localtime=session['theDate'], obsessions=obsessionList, triggers=triggerList, places=placeList )
    #return "calendar genereated"
    erpFrequencyGraphs=ERPGraphs(frequencies)

    erpYearGraphFunctions=Markup(erpFrequencyGraphs['yearChartFunctions'])

    erpMonthChartFunctions=Markup(erpFrequencyGraphs['monthChartFunctions'])
    erpMonthChartsToDraw=Markup(erpFrequencyGraphs['monthChartsToDraw'])
    erpMonthChartDivs=Markup(erpFrequencyGraphs['monthChartDivs'])
    erpByMonthFrequencySelector=Markup(erpFrequencyGraphs['monthSelector'])

    erpByWeekChartDivs=Markup(erpFrequencyGraphs['weekDivs'])
    erpByWeekChartFunctions=Markup(erpFrequencyGraphs['weekChartFunctions'])

    hwPills=Markup(hwPills)
    hwPanes=Markup(hwPanes)
    hwByMonthList=""
    hwByTriggerList="[['Obsession', 'Number'],"
    for k,v in hws.iteritems() :
        hwByObsessionList+="['"+v[0].replace("'","\\'").replace('"','\\"')+"',"+str(v[1])+"],"
    hwByObsessionList+="]"
    hwByObsessionList=Markup(hwByObsessionList)

    for k,v in trggrs.iteritems() :
        hwByTriggerList+="['"+v[0].replace("'","\\'").replace('"','\\"')+"',"+str(v[1])+"],"
    hwByTriggerList+="]"
    hwByTriggerList=Markup(hwByTriggerList)


    first=True
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    for k,v in hwsByMonth.iteritems() :
        #if first :
        #    hwByMonthList+="["+str(v[0]-1)+",0],"
        hwByMonthList+="['"+monthDict[v[0]]+"',"+str(v[1])+"],"
    #hwByMonthList+="]"
    hwByMonthList=Markup(hwByMonthList)
    #generate calendar for patient


    episodeList=[]
    #episodes=Episode.query(Episode.userID==patientCode)
    eps={}
    trggrs={}
    episodesByMonth={}
    episodePills=""
    episodePanes=""
    isFirst=True
    obsessionOccurences={}
    episodeFrequencies={}
    episodeItensities={}
    episodesSorted=sorted(episodes, key=(lambda g : g.dateTime))
    episodesSorted.reverse()
    for episode in episodesSorted :
        erpDate=datetime.datetime.strptime(episode.dateTime[:10], '%Y-%m-%d')

        if episodeFrequencies.get(str(erpDate.year), False) :
            if episodeFrequencies[str(erpDate.year)].get(str(erpDate.isocalendar()[1]), False) :
                if episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])].get(str(erpDate.isocalendar()[2]), False) :
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']+=['p']
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']+=1
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']+=1
                    episodeFrequencies[str(erpDate.year)]['number']+=1
                else :
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']=['p']
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                    episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']+=1
                    episodeFrequencies[str(erpDate.year)]['number']+=1
            else :
                episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]={}
                episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']=['p']
                episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']=1
                episodeFrequencies[str(erpDate.year)]['number']+=1

        else :
            episodeFrequencies[str(erpDate.year)]={}
            episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]={}
            episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
            episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['eps']=['p']
            episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
            episodeFrequencies[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']=1
            episodeFrequencies[str(erpDate.year)]['number']=1

        if episodeItensities.get(str(erpDate.year), False) :
            if episodeItensities[str(erpDate.year)].get(str(erpDate.isocalendar()[1]), False) :
                if episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])].get(str(erpDate.isocalendar()[2]), False) :
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['total']+=episode.intensity
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']+=1
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']+=1
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['total']+=episode.intensity
                    episodeItensities[str(erpDate.year)]['number']+=1
                    episodeItensities[str(erpDate.year)]['total']+=episode.intensity
                else :
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['total']=episode.intensity
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']+=1
                    episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['total']+=episode.intensity
                    episodeItensities[str(erpDate.year)]['number']+=1
                    episodeItensities[str(erpDate.year)]['total']+=episode.intensity
            else :
                episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]={}
                episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
                episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['total']=episode.intensity
                episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
                episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']=1
                episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['total']=episode.intensity
                episodeItensities[str(erpDate.year)]['number']+=1
                episodeItensities[str(erpDate.year)]['total']+=episode.intensity

        else :
            episodeItensities[str(erpDate.year)]={}
            episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]={}
            episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]={}
            episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['total']=episode.intensity
            episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])][str(erpDate.isocalendar()[2])]['number']=1
            episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['number']=1
            episodeItensities[str(erpDate.year)][str(erpDate.isocalendar()[1])]['total']=episode.intensity
            episodeItensities[str(erpDate.year)]['number']=1
            episodeItensities[str(erpDate.year)]['total']=episode.intensity





        #if episode.time=
        if obsessionOccurences.get(episode.obsession, False) :
            if int(episode.time[-8:-6])<17:
                obsessionOccurences[episode.obsession].night+=1
        episodeDate=datetime.datetime.strptime(episode.dateTime[:10], '%Y-%m-%d')
        #add to episodePills 
        episodeID=episode.episodeID.replace('/','slashed').replace(' ','spacing').replace(':','colon').replace('-','dash')
        if isFirst :
            row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+episodeID+'">'
        else :
            row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+episodeID+'">'
        row+=episode.dateTime[:10]+'</a></li>'
        episodePills+=row

        if isFirst :
            row='<div id="'+episodeID+'" class="tab-pane fade in active">'
            isFirst=False
        else :
            row='<div id="'+episodeID+'" class="tab-pane fade in">'

        theCompulsion=episode.compulsion
        if not episode.compulsion :
            theCompulsion="No Data"
        theTrigger=episode.trigger
        if not episode.trigger :
            theTrigger="No Data"
        theObsession=episode.obsession
        if not episode.obsession :
            theObsession="No Data"


        heartRate="No Data"
        if episode.heartRate!=0 :
            heartRate=str(episode.heartRate)+" BPM"

        place="No data"
        if episode.place != "" :
            place=episode.place
        anxietyLevel="No Data"
        if episode.intensity!="" :
            anxietyLevel=str(episode.intensity)

        timeSpent=""
        if (int(episode.resistanceTime) )/60 >=1:
            timeSpent=str(int(episode.resistanceTime)/60)+" minutes "+str(int(episode.resistanceTime) % 60)+" seconds"
        else :
            timeSpent=str(episode.resistanceTime)+" Seconds"




        row+='<table class="table table-bordered table-striped">'
        row+='<th colspan=\'2\' style=\'text-align:center !important\'>Episode Summary </th>'
        row+='<tr><td><strong>Date</strong>:</td><td><strong>Time</strong>:</td></tr>'
        row+='<tr><td class="smaller">'+episode.dateTime[:10]+'</td><td class="smaller">'+episode.time+'</td></tr>'
        row+='<tr><td><strong>Obsession</strong>:</div><td><strong>Trigger</strong>:</div></tr>'
        row+='<tr><td class="smaller">'+theObsession+'</td><td class="smaller">'+theTrigger+'</td></tr>'
        row+='<tr><td><strong>Compulsion</strong>:</div><td><strong>Time Spent</strong>:</div></tr>'
        row+='<tr><td class="smaller">'+theCompulsion+'</td><td class="smaller">'+timeSpent+'</td></tr>'  
        row+='<tr><td><strong>Intensity</strong>:</div><td><strong>Heart Rate</strong>:</div></tr>'
        row+='<tr><td class="smaller">'+anxietyLevel+'</td><td class="smaller">'+heartRate+'</td></tr>' 
        row+='</table>'            

        
        episodePanes+=row+"</div>"
        episodeTemp={}
        temp=eps.get(episode.obsession, False)
        if theObsession!="No Data" :
            if temp :
                eps[episode.obsession]=[eps[episode.obsession][0],eps[episode.obsession][1]+1]
            else :
                eps[episode.obsession]=[episode.obsession,1]
        
        temp=trggrs.get(episode.trigger, False)
        if theTrigger!="No Data" :
            if temp :
                trggrs[episode.trigger]=[trggrs[episode.trigger][0],trggrs[episode.trigger][1]+1]
            else :
                trggrs[episode.trigger]=[episode.trigger,1]
        
        episodeWeekDate=datetime.datetime.strptime(episode.dateTime[:10], '%Y-%m-%d').date()
        temp=episodesByMonth.get(episodeWeekDate.month, False)
        if temp :
            episodesByMonth[episodeWeekDate.month]=[episodesByMonth[episodeWeekDate.month][0],episodesByMonth[episodeWeekDate.month][1]+1]
        else :
            episodesByMonth[episodeWeekDate.month]=[episodeWeekDate.month,1]
        episodeTemp['episodeID']=episode.episodeID
        episodeTemp['userID']=episode.userID
        episodeTemp['obsession']=episode.obsession
        if episode.obsession :
            episodeTemp['obsession']=episode.obsession.replace('"',"&quot;").replace("'","&#39;")
        episodeTemp['trigger']=episode.trigger
        if episode.trigger :
            episodeTemp['trigger']=episode.trigger.replace('"',"&quot;").replace("'","&#39;")
        episodeTemp['place']=episode.place
        episodeTemp['time']=episode.time
        episodeTemp['dateTime']=episode.dateTime
        episodeTemp['place']=episode.place
        episodeTemp['intensity']=episode.intensity
        episodeTemp['resistanceTime']=episode.resistanceTime
        episodeList.append(episodeTemp)
    


    episodeFrequencyGraphs=EpisodeGraphs(episodeFrequencies)

    episodeYearGraphFunctions=Markup(episodeFrequencyGraphs['yearChartFunctions'])

    episodeMonthChartFunctions=Markup(episodeFrequencyGraphs['monthChartFunctions'])
    episodeMonthChartsToDraw=Markup(episodeFrequencyGraphs['monthChartsToDraw'])
    episodeMonthChartDivs=Markup(episodeFrequencyGraphs['monthChartDivs'])
    episodeByMonthFrequencySelector=Markup(episodeFrequencyGraphs['monthSelector'])



    episodePills=Markup(episodePills)
    episodePanes=Markup(episodePanes)
    episodeByMonthList=""
    episodeByObsessionList="[['Obsession', 'Number'],"
    episodeByTriggerList="[['Trigger', 'Number'],"
    for k,v in eps.iteritems() :
        episodeByObsessionList+="['"+v[0].replace("'","\\'").replace('"','\\"')+"',"+str(v[1])+"],"
    episodeByObsessionList+="]"
    episodeByObsessionList=Markup(episodeByObsessionList)

    for k,v in trggrs.iteritems() :
        episodeByTriggerList+="['"+v[0].replace("'","\\'").replace('"','\\"')+"',"+str(v[1])+"],"
    episodeByTriggerList+="]"
    episodeByTriggerList=Markup(episodeByTriggerList)


    first=True
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    for k,v in episodesByMonth.iteritems() :
        #if first :
        #    episodeByMonthList+="["+str(v[0]-1)+",0],"
        episodeByMonthList+="['"+monthDict[v[0]]+"',"+str(v[1])+"],"
    #episodeByMonthList+="]"
    episodeByMonthList=Markup(episodeByMonthList)
    #generate calendar for patient
    session['triggerList']  =triggerList
    session['obsessionList']=obsessionList
    session['placeList']    =placeList
    session['erpHWList']    =erpHWList

    #if episodeByTriggerList=="[['Trigger', 'Number'],]" :
    #    episodeByTriggerList="[]"
    #if episodeByObsessionList=="[['Obsession', 'Number'],]" :
    #    episodeByObsessionList="[]"
    #monthCalendars=generateCalendar(erpHWList, localtime=session['theDate'], obsessions=obsessionList, triggers=triggerList, places=placeList )
    monthCalendars=generateCalendars(erpHWs=erpHWDict, localtime=session['theDate'], obsessions=obsessionList, triggers=triggerList, places=placeList )
    #return "everything but calendar generated"
    return render_template('patientPage2.html', numRequests=session['numRequests'], 
                                                frequencies=Markup(json.dumps(frequencies)),
                                                erpByWeekChartFunctions=erpByWeekChartFunctions,
                                                erpByWeekChartDivs=erpByWeekChartDivs,
                                                #episodeYearChartDivs=episodeYearChartDivs,
                                                erpYearGraphFunctions=erpYearGraphFunctions,
                                                episodeYearGraphFunctions=episodeYearGraphFunctions,
                                                erpByMonthFrequencySelector=erpByMonthFrequencySelector,
                                                episodeByMonthFrequencySelector=episodeByMonthFrequencySelector,
                                                #drawEpisodeYearGraphFunctions=drawEpisodeYearGraphFunctions,
                                                episodeMonthChartDivs=episodeMonthChartDivs,
                                                episodeMonthChartFunctions=episodeMonthChartFunctions,
                                                episodeMonthChartsToDraw=episodeMonthChartsToDraw,
                                                #drawERPYearGraphFunctions=drawERPYearGraphFunctions,
                                                erpMonthChartFunctions=erpMonthChartFunctions,
                                                erpMonthChartDivs=erpMonthChartDivs,
                                                erpMonthChartsToDraw=erpMonthChartsToDraw,
                                                episodePills=episodePills,episodePanes=episodePanes, 
                                                ERPHWPills=hwPills,ERPHWPanes=hwPanes, 
                                                hwByMonthList=hwByMonthList, 
                                                episodeByMonthList=episodeByMonthList,
                                                episodeByObsessionList=episodeByObsessionList ,
                                                episodeByTriggerList=episodeByTriggerList, 
                                                hwByObsessionList=hwByObsessionList, 
                                                hwByTriggerList=hwByTriggerList, 
                                                patientCode=patientCode, currMonth=currMonth, notePills=notePills, notePanes=notePanes, noteForm=noteForm,noteFormError=None, noteFormSuccess="Success",hideDanger='hidden ', monthCalendars=monthCalendars, patient=patient, obsessionPills=obsessionPills, obsessionPanes=obsessionPanes)


#Login Page
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
        if specialist.password!=Hasher(form.password.data) :
            return render_template('login.html', form=form, error="Incorrect password")
        if not specialist.emailVerified :
            return render_template('verifyEmail.html')
        session['numRequests']=specialist.numberRequests
        session['verified']=specialist.verified
        session['logged_in']=True
        session['specialistID']=form.email.data
        session['specialistEmail']=specialist.email
        session['theDate']=datetime.datetime.fromtimestamp(float(form.date.data)/1000.0)
        return myPatients()
    return render_template('login.html', form=form)


@app.route('/scheduleAppointment', methods=['GET','POST']) 
def scheduleAppointment():
    if not session.get('logged_in',False) :
        return login
    form=ScheduleAppForm()
    specialist=Specialist.get_by_id(session['specialistID'])
    codes=json.loads(specialist.patientCodes)
    users=""
    for patientCode in codes :
        patient=Patient.get_by_id(patientCode)
        users+='<option value="'+patientCode+'">'+Unhash(patient.name)+'</option>'
    users=Markup(users)
    if request.method!='POST':
        return render_template('scheduleAppointment.html',numRequests=specialist.numberRequests, form=form, users=users)
    form=ScheduleAppForm(request.form)
    pat=None
    try :
        pat=Patient.get_by_id(form.userID.data)
    except :
        form=ScheduleAppForm()
        return render_template('scheduleAppointment.html',numRequests=specialist.numberRequests, form=form, users=users, error="Please choose a valid patient")
    if pat :
        theDate=None
        try :
            theDate=datetime.datetime.strptime(form.dated.data, '%Y-%m-%d')
        except :
            form=ScheduleAppForm()
            return render_template('scheduleAppointment.html', numRequests=specialist.numberRequests,form=form, users=users, error="There was an error with your date format")
        if theDate<session['theDate'] :
            form=ScheduleAppForm()
            return render_template('scheduleAppointment.html',numRequests=specialist.numberRequests, form=form, users=users, error="Please enter a valid date")
        if pat.nextAppointment<= str(session['theDate']) :
            pat.lastAppointment=patient.nextAppointment
        pat.nextAppointment=str(theDate.date())+" "+form.time.data
        #pat.name=pat.name
        pat.put()
        sender=session['specialistEmail']
        recipient=Unhash(pat.email)
        subject=specialist.name+" has scheduled an appointment for"+pat.nextAppointment
        text="An appointment as been schedule for you on "+pat.nextAppointment+" with "+specialist.name
        emailSent=sendEmail(sender=sender, recipient=recipient, subject=subject,html="",text=text)
        return render_template('appointmentConfirmation.html',numRequests=specialist.numberRequests, patientName=Unhash(pat.name), theDate=pat.nextAppointment)
    else :
        form=ScheduleAppForm()
        return render_template('scheduleAppointment.html',numRequests=specialist.numberRequests, form=form, users=users, error="Please choose a valid patient")
    return render_template('scheduleAppointment.html', numRequests=specialist.numberRequests,form=form,users=users, error="There was an error processing your request please try again")



# log user out clear session
@app.route('/logout')
def logout() :
    session.clear()
    return home()


#save a note 
@app.route('/saveNote', methods=['GET', 'POST'])
def saveNote() :

    #form=EnterNoteForm(request.form)
    #if not form.validate() :
    #    return "pop" #render_template('newNote.html', noteForm=form, noteFormError="Something went wrong", hideDanger="")
    #newNote=Note(id=form.noteID.data, noteID=form.noteID.data, note=form.note.data,specialistID=session['specialistID'], userID=session.get('userID'), dateTime=str(session['theDate']))
    #newNote.put()
    try :
        newNote=Note(id=request.form['noteID'], noteID=request.form['noteID'], note=request.form['note'],specialistID=session['specialistID'], userID=session.get('userID'), dateTime=str(session['theDate']))
        newNote.put()
    except :
        form=EnterNoteForm(request.form)
        return render_template('newNote.html', noteForm=form, noteFormError="Something went wrong", hideDanger="")
    theForm=EnterNoteForm()
    aForm=EnterNoteForm()
    return render_template('newNote.html', noteForm=aForm,noteFormError=None, noteFormSuccess="Success", hideDanger="hidden ")


@app.route('/saveEditNote/<noteID>', methods=['GET', 'POST'])
def saveEditNote(noteID) :
    form=editNoteForm(request.form)
    if not form.validate() :
        return render_template('editNoteForm.html', noteForm=form, noteFormError="Something went wrong", hideDanger="")
    oldNote=ndb.Key('Note', noteID)
    oldNote.delete()
    #oldNote=oldNote.get()
    #oldNote.noteID=form.noteID.data
    #oldNote.oldNoteID=form.noteID.data
    #oldNote.key=form.noteID.data
    #oldNote.note=id=form.note.data
    #oldNote.put()
    newNote=Note(id=form.noteID.data, noteID=form.noteID.data, note=form.note.data,specialistID=session['specialistID'], userID=session.get('userID'), dateTime=str(session['theDate']))
    newNote.put()
    return "successs"


@app.route('/removeNote/<noteID>')
def removeNote(noteID) :
    if not session.get('logged_in', False) :
        return render_template('page_not_found.html'), 500
    oldNote=ndb.Key('Note', noteID)
    oldNote.delete()
    return "ll"


#get note pane for current userID
@app.route('/getNotePane')
def getNotePane() :
    #verify logged in
    
    if not session.get('userID', False) :
        return "error", 400
    #Load patient data
    patient=Patient.get_by_id(session["userID"])

    if not patient :
        return "error", 400

    #generate note pills and panes
    notes=Note.query(Note.userID==session['userID'], Note.specialistID==session['specialistID'])
    notePills=[]
    notePanes=[]
    isFirst=True
    noteNum=0
    for note in notes :
        if isFirst :
            row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+note.noteID.replace('#','aHashTag').replace(' ', '_')+'">'
        else :
            row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+note.noteID.replace('#','aHashTag').replace(' ', '_')+'">'
        row+=note.noteID+'</a></li>'
        notePills.append(Markup(row))
        tempID=note.noteID.replace('#','aHashTag').replace(' ', '_')
        if isFirst :
            row='<div id="'+tempID+'" class="tab-pane fade in active note-pane"><center>'
            isFirst=False
        else :
            row='<div id="'+tempID+'" class="tab-pane fade in note-pane"><center>'
  
        pop="""<div class="btn-toolbar" data-role="editor-toolbar" data-target="#"""+tempID+"""yyeeeeejfdjd">
            <div class="btn-group">
                <a class="btn dropdown-toggle" data-toggle="dropdown" title="" data-original-title="Font"><i class="icon-font"></i><b class="caret"></b></a>
                    <ul class="dropdown-menu">
                    <li><a data-edit="fontName Serif" style="font-family:'Serif'">Serif</a></li><li><a data-edit="fontName Sans" style="font-family:'Sans'">Sans</a></li><li><a data-edit="fontName Arial" style="font-family:'Arial'">Arial</a></li><li><a data-edit="fontName Arial Black" style="font-family:'Arial Black'">Arial Black</a></li><li><a data-edit="fontName Courier" style="font-family:'Courier'">Courier</a></li><li><a data-edit="fontName Courier New" style="font-family:'Courier New'">Courier New</a></li><li><a data-edit="fontName Comic Sans MS" style="font-family:'Comic Sans MS'">Comic Sans MS</a></li><li><a data-edit="fontName Helvetica" style="font-family:'Helvetica'">Helvetica</a></li><li><a data-edit="fontName Impact" style="font-family:'Impact'">Impact</a></li><li><a data-edit="fontName Lucida Grande" style="font-family:'Lucida Grande'">Lucida Grande</a></li><li><a data-edit="fontName Lucida Sans" style="font-family:'Lucida Sans'">Lucida Sans</a></li><li><a data-edit="fontName Tahoma" style="font-family:'Tahoma'">Tahoma</a></li><li><a data-edit="fontName Times" style="font-family:'Times'">Times</a></li><li><a data-edit="fontName Times New Roman" style="font-family:'Times New Roman'">Times New Roman</a></li><li><a data-edit="fontName Verdana" style="font-family:'Verdana'">Verdana</a></li></ul>
            </div>
            <div class="btn-group">
                <a class="btn dropdown-toggle" data-toggle="dropdown" title="" data-original-title="Font Size"><i class="icon-text-height"></i>&nbsp;<b class="caret"></b></a>
          <ul class="dropdown-menu">
          <li><a data-edit="fontSize 5"><font size="5">Huge</font></a></li>
          <li><a data-edit="fontSize 3"><font size="3">Normal</font></a></li>
          <li><a data-edit="fontSize 1"><font size="1">Small</font></a></li>
          </ul>
            </div>
            <div class="btn-group">
                <a class="btn" data-edit="bold" title="" data-original-title="Bold (Ctrl/Cmd+B)"><i class="icon-bold"></i></a>
                <a class="btn" data-edit="italic" title="" data-original-title="Italic (Ctrl/Cmd+I)"><i class="icon-italic"></i></a>
                <a class="btn" data-edit="strikethrough" title="" data-original-title="Strikethrough"><i class="icon-strikethrough"></i></a>
                <a class="btn" data-edit="underline" title="" data-original-title="Underline (Ctrl/Cmd+U)"><i class="icon-underline"></i></a>
            </div>
            <div class="btn-group">
                <a class="btn" data-edit="insertunorderedlist" title="" data-original-title="Bullet list"><i class="icon-list-ul"></i></a>
                <a class="btn" data-edit="insertorderedlist" title="" data-original-title="Number list"><i class="icon-list-ol"></i></a>
                <a class="btn" data-edit="outdent" title="" data-original-title="Reduce indent (Shift+Tab)"><i class="icon-indent-left"></i></a>
                <a class="btn" data-edit="indent" title="" data-original-title="Indent (Tab)"><i class="icon-indent-right"></i></a>
            </div>
            <div class="btn-group">
                <a class="btn" data-edit="justifyleft" title="" data-original-title="Align Left (Ctrl/Cmd+L)"><i class="icon-align-left"></i></a>
                <a class="btn" data-edit="justifycenter" title="" data-original-title="Center (Ctrl/Cmd+E)"><i class="icon-align-center"></i></a>
                <a class="btn" data-edit="justifyright" title="" data-original-title="Align Right (Ctrl/Cmd+R)"><i class="icon-align-right"></i></a>
                <a class="btn" data-edit="justifyfull" title="" data-original-title="Justify (Ctrl/Cmd+J)"><i class="icon-align-justify"></i></a>
            </div>
            <div class="btn-group">
                <a class="btn dropdown-toggle" data-toggle="dropdown" title="" data-original-title="Hyperlink"><i class="icon-link"></i></a>
                <div class="dropdown-menu input-append">
                    <input class="span2" placeholder="URL" type="text" data-edit="createLink">
                    <button class="btn" type="button">Add</button>
                </div>
                <a class="btn" data-edit="unlink" title="" data-original-title="Remove Hyperlink"><i class="icon-cut"></i></a>
            </div>
      
            <div class="btn-group">
                <a class="btn" title="" id="pictureBtn" data-original-title="Insert picture (or just drag &amp; drop)"><i class="icon-picture"></i></a>
                <input type="file" data-role="magic-overlay" data-target="#pictureBtn" data-edit="insertImage" style="opacity: 0; position: absolute; top: 0px; left: 0px; width: 41px; height: 30px;">
            </div>
            <div class="btn-group">
                <a class="btn" data-edit="undo" title="" data-original-title="Undo (Ctrl/Cmd+Z)"><i class="icon-undo"></i></a>
                <a class="btn" data-edit="redo" title="" data-original-title="Redo (Ctrl/Cmd+Y)"><i class="icon-repeat"></i></a>
            </div>
            <input type="text" data-edit="inserttext" id="voiceBtn" x-webkit-speech="" style="display: none;">
        </div>"""
        #    <div class="noteEditor" contenteditable="true" id=\""""+tempID+'yyeeeeejfdjd">'+note.note.replace('&nbsp', ' ')+'</div>'
            #row+=note.note.replace('\n','<br>').replace(' ', '&nbsp')
        tempNote=editNoteForm()
        tempNote.noteID.data=note.noteID
        tempNote.oldNoteID.data=note.noteID
        row+=render_template('editNoteForm.html', noteForm=tempNote, note=Markup(note.note), noteNum=noteNum)
        noteNum+=1
        row+='</center></div>'

        notePanes.append(Markup(row))
    return render_template('notePills.html', notePills=notePills, notePanes=notePanes)


@app.route('/removeERP/<HWID>')
def removeERP(HWID) :
    if not session.get('logged_in', False) :
        return render_template('page_not_found.html')
    hws=ERPHW.query(ERPHW.HWID==(HWID.replace("%"," ")[:10].replace('-','/')+HWID.replace("%"," ")[10:]))
    for hw in hws :
        hw.key.delete()
    form_fields = {
        "scheduledID": HWID,
    }
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url=urlForERPRemove,
    payload=form_data,
    method=urlfetch.POST,
    headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if result.status_code!= 200 :
        return "lop"
    return "ll"


@app.route('/addERPHomework', methods=['POST'])
def addERPHomework() :
    if not session.get('logged_in', False) :
        return render_template('page_not_found.html')
    patientCode=session.get('userID', False)
    
    if not patientCode :
        return render_template('page_not_found.html')
    form=addERPHWForm(request.form)    

    isNight= 'PM'==form.time.data[-2:]
    newHour=form.time.data[:2] 
    restTime=form.time.data[2:-2]
    hour=int(newHour)
    if isNight :
        if hour!= 12 :
            newHour= int(newHour)+12
    else :
        if hour==12 :
            newHour=24
    militTime=str(newHour)+restTime
    dateTime=datetime.datetime.strptime((form.localtime.data+" "+militTime),'%Y-%m-%d %H:%M')
    dateTime=str(dateTime) #str(dateTime)[:10]+" "+str(dateTime)[11:]
    obsession=Unhash(form.obsessions.data.split(":{}:{}{4")[1])
    obsessionID=form.obsessions.data.split(":{}:{}{4")[0]
    trigger=Unhash(form.triggers.data.split(":{}:{}{4")[1])
    theTrigger="No Data"
    triggerID=None
    if trigger :
        triggerID=form.triggers.data.split(":{}:{}{4")[0]
        theTrigger=Unhash(form.triggers.data.split(":{}:{}{4")[1])


    hwID=dateTime+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    erpHW=ERPHW(HWID=hwID,triggerID=triggerID,obsessionID=obsessionID,userID=patientCode, status="Incomplete", obsession= form.obsessions.data, trigger=theTrigger, place=form.places.data, prompt=form.prompt.data, time=form.time.data, dateTime=dateTime )
    #erpHW.put()
    form_fields = {
        "id": hwID,
        "scheduledDate": dateTime,
        "obssesion": obsession,
        "trigger": theTrigger,
        "obsessionID": obsessionID,
        "triggerID": triggerID,
        "userID": Unhash(patientCode)
    }
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url=urlForERPAdd,
    payload=form_data,
    method=urlfetch.POST,
    headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return result.content
    if result.status_code!= 200 :
        return "error Page"
    return viewPatient(patientCode)
    erpTemp={}
    erpTemp['HWID']=erpHW.HWID
    erpTemp['userID']=erpHW.userID
    erpTemp['status']=erpHW.status
    erpTemp['obsession']=erpHW.obsession
    erpTemp['trigger']=erpHW.trigger
    erpTemp['place']=erpHW.place

    erpTemp['prompt']=erpHW.prompt
    erpTemp['time']=erpHW.time
    erpTemp['dateTime']=erpHW.dateTime
    session['erpHWList'].append(erpTemp)
    session['erpHWList'].sort(key=lambda x: x.HWID)

    monthCalendars=generateCalendar(erpHWs=session['erpHWList'], localtime=session['theDate'], obsessions=session['obsessionList'], triggers=session['triggerList'], places=session['placeList'] )
    return render_template('calendar.html', monthCalendars=monthCalendars)


#Handles new App User Information from Post
#Will contain special passcode from app
@csrf.exempt
@app.route('/users', methods=['GET', 'POST'])
def registerAppUser():
    err=Errorr(error="registeringUser"+json.dumps(request.form))
    err.put()
    if request.method!="POST" :
        return render_template('page_not_found.html')
    try :
        confirmationCode=request.form['confirmationCode'] #request.form.get('confirmationCode',False)
        if not confirmationCode :
            err=Errorr(error="Missing ConfirmationCode"+json.dumps(request.form))
            err.put()
            return "confirmationCode Missing", 400 
        if confirmationCode!=secretKey :
            responseData={}
            response['error']="User not registered"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=400, mimetype="application/json")
        try :
            newPatient=Patient(firstName=Hasher(request.form['firstName']), 
                               lastName=Hasher(request.form['lastName']),  
                               name=Hasher(request.form['firstName']+" "+request.form['lastName']), 
                               email=Hasher(request.form['email']), 
                               uniqueID=Hasher(request.form['userID']), 
                               id=Hasher(request.form['userID']), 
                               nextAppointment=None, episodes=0)
            newPatient.put()
        except :
            return "Error on server", 500
        responseData={}
        responseData['registered']="Success"
        responsedata=json.dumps(responseData)
        return Response(response=responsedata, status=201, mimetype="application/json")
    except :
        content=json.loads(request.form['u'])
        errerr=Errorr(error="Attempting as Json"+json.dumps(content))
        errerr.put()
        form=json.loads(request.form['u'])
        confirmationCode=form.get('confirmationCode',False)
        if not confirmationCode :
            err=Errorr(error="No ConfirmationCode in JSON attempt"+json.dumps(form))
            err.put()
            return "confirmationCode Missing", 400 
        if confirmationCode!=secretKey :
            err=Errorr(error="ConfirmationCode doesnt match"+json.dumps(form))
            err.put()
            responseData={}
            response['error']="User not registered"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=400, mimetype="application/json")
        
        newPatient=Patient(firstName=Hasher(request.form['firstName']), 
                               lastName=Hasher(request.form['lastName']),  
                               name=Hasher(request.form['firstName']+" "+request.form['lastName']), 
                               email=Hasher(request.form['email']), 
                               uniqueID=Hasher(request.form['userID']), 
                               id=Hasher(request.form['userID']), 
                               nextAppointment=None, episodes=0)
        newPatient.put()
        err=Errorr(error="Registered patient via JSon"+json.dumps(form))
        err.put()        
        responseData={}
        responseData['registered']="Success"
        responsedata=json.dumps(responseData)
        return Response(response=responsedata, status=201, mimetype="application/json")

@app.route('/registerPatient/<requestID>')
def registerPatient (requestID) :
    if not session['logged_in'] :
        return "oops"
    requestee=Request.get_by_id(int(requestID))

    specialist=Specialist.get_by_id(requestee.specialistID)

    codes=json.loads(specialist.patientCodes)
    if not requestee.userID in codes :
        codes.append(requestee.userID)
        specialist.patientCodes=json.dumps(codes)
        specialist.put()

    requestee.key.delete()

    specialist.numberRequests-=1
    session['numRequests']-=1
    specialist.put()
    return render_template('patientConfirmed.html', numRequests=session['numRequests'],patientName=Unhash(requestee.patientName))

@app.route('/denyPatient/<requestID>')
def denyPatient (requestID) :
    if not session['logged_in'] :
        return "oops"
    requestee=Request.get_by_id(int(requestID))

    specialist=Specialist.get_by_id(requestee.specialistID)

    #specialist.patientCodes.append(request.userID)
    #specialist.put()
    requestee.key.delete()
    specialist.numberRequests-=1
    session['numRequests']-=1
    specialist.put()
    return viewRequests()

@csrf.exempt
@app.route('/therapistrequests/<therapistEmail>', methods=['GET','POST'])
def requestToTherapist(therapistEmail):
    err=Errorr(error="Request Sent to Therapist "+therapistEmail+" "+json.dumps(request.form))
    err.put()
    try :
        if request.method!="POST" :
            return render_template('page_not_found.html')
        if request.form['confirmationCode']!=secretKey :
            responseData={}
            responseData['error']="uh oh"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=400, mimetype="application/json")
        specialist=Specialist.get_by_id(therapistEmail)
        if not specialist :
            responseData={}
            responseData['error']="Therapist email not found"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=404, mimetype="application/json")
        lastName=request.form['patientLastName']
        userID=request.form['userID']
        firstName=request.form['patientFirstName']
        fullName=firstName+" "+lastName
        patient=Patient.get_by_id(userID)
        if not patient :
            form_fields = {
                "userID": userID
            }
            form_data = urllib.urlencode(form_fields)
            result = urlfetch.fetch(url=urlForUserInfo,
            payload=form_data,
            method=urlfetch.POST,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
            results=json.loads(result.content)
            content=results['info']
            newPatient=Patient(id=userID, firstName=Hasher(content['firstName']),
                                lastName=Hasher(content['lastName']),
                                name= Hasher(fullName),
                                email=Hasher(content['email']),
                                uniqueID=Hasher(content['userID']),
                                nextAppointment=None,
                                episodes=0,
                                resistanceTime=None)
            newPatient.put()
        newRequest=Request(specialistID=therapistEmail, patientName=Hasher(fullName), userID=Hasher(userID))
        newRequest.put()
        test=Errorr(error="popopop"+Hasher(fullName))
        test.put()
        specialist.numberRequests+=1
        #session['numRequests']+=1
        specialist.put()
        responseData={}
        responseData['success']="Request registered"
        responseData=json.dumps(responseData)
        return Response(response=responseData, status=201, mimetype="application/json")
    except :
        content=json.loads(request.form['u'])
        errerr=Errorr(error="Registering Request Via JSON for "+therapistEmail+" "+content['userID'])
        errerr.put()
        form=json.loads(request.form['u'])
        #eee=Errorr(error="Continuing JSON Attempt"+str(form.keys()))
        #eee.put()
        if request.method!="POST" :
            return render_template('page_not_found.html')
        if form['confirmationCode']!=secretKey :
            responseData={}
            responseData['error']="uh oh"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=400, mimetype="application/json")
        #eee=Errorr(error="CCODe present")
        #eee.put()
        specialist=Specialist.get_by_id(therapistEmail)
        if not specialist :
            responseData={}
            responseData['error']="Therapist email not found"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=404, mimetype="application/json")
        lastName=form['lastName']
        userID=form['userID']
        firstName=form['firstName']
        fullName=firstName+" "+lastName
        email=form['email']
        eee=Errorr(error="Attempting Request from "+userID+" "+fullName+" For therapist "+therapistEmail)
        eee.put()
        patient=Patient.get_by_id(userID)
        try :
            form_fields = {
                "userID": userID,
            }
            form_data = urllib.urlencode(form_fields)
            result = urlfetch.fetch(url=urlForUserInfo,
            payload=form_data,
            method=urlfetch.POST,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
            eep=Errorr(error="Request post done "+userID)
            eep.put()
            results=json.loads(result.content)
            content=results['info']
            eep=Errorr(error="About to Place patient "+userID+fullName)
            eep.put()
            newPatient=Patient(id=Hasher(userID), firstName=Hasher(content['firstName']),
                                lastName=Hasher(content['lastName']),
                                name= Hasher(fullName),
                                email=Hasher(content['email']),
                                uniqueID=Hasher(content['userID']),
                                nextAppointment=None,
                                episodes=0,
                                resistanceTime=None)
            newPatient.put()
            eee=Errorr(error="Patient Registered "+fullName)
            eee.put()
            newRequest=Request(specialistID=therapistEmail, patientName=Hasher(fullName), userID=Hasher(userID))
            newRequest.put()
            specialist.numberRequests+=1
            erort=Errorr(error="Patient "+ fullName+" request for "+therapistEmail+" registered successfuly")
            #session['numRequests']+=1
            specialist.put()
            erort.put()
            eee=Errorr(error="Testingsasa")
            eee.put()
        except :
            erort=Errorr(error="Patient "+ fullName+" request for "+therapistEmail+" failed")
            erort.put()
            responseData={}
            responseData['success']="Failed"
            responseData=json.dumps(responseData)
            return Response(response=responseData, status=500, mimetype="application/json")
        responseData={}
        responseData['success']="Request registered"
        responseData=json.dumps(responseData)
        return Response(response=responseData, status=201, mimetype="application/json")

@csrf.exempt
@app.route('/getData', methods=['GET','POST'])
def getData():
    if request.method!="POST" :
        return render_template('page_not_found.html'), 500
    if request.form.superSecretConfirmationKey!=secretKey :
        return render_template('page_not_found.html'), 500
    user=ndb.Key('Patient', request.form['userID'])
    user=user.get()
    if user.password!=request.form['userPassword'] :
        return render_template('page_not_found.html'), 500
    hws=ERPHW.query(ERPHW.userID==request.form['userID'], ERPHW.new==True)
    respDict={}
    respDict['resistanceTime']=user.resistanceTime
    respDict['hwList']=[]
    for hw in hws :
        hw.new=False
        hw.put()
        erpTemp={}
        #erpTemp['HWID']=hw.HWID
        erpTemp['userID']=hw.userID
        #erpTemp['status']=hw.status
        erpTemp['obsession']=hw.obsession
        erpTemp['trigger']=hw.trigger
        erpTemp['place']=hw.place
        erpTemp['notes']=hw.prompt
        erpTemp['scheduledDate']=hw.dateTime
        erpTemp['obsessionID']=hw.obsessionID
        erpTemp['triggerID']=hw.triggerID
        respDict['hwList'].append(erpTemp)   
    responseData=json.dumps(respDict)
    return Response(response=responseData, status=200, mimetype="application/json")


@csrf.exempt
@app.route('/uploadData')
def uploadData():
    if request.method!="POST" :
        return render_template('page_not_found.html'), 500
    if request.form.superSecretConfirmationKey!=secretKey :
        return render_template('page_not_found.html'), 500
    newHwsList=json.loads(request.form['erpHWList'])
    newEpisodesList=json.loads(request.form['epsisodeList'])
    newObsessionsList=json.loads(request.form['obsessionList'])
    newTriggersList=json.loads(request.form['triggerList'])
    newCompulsionsList=json.loads(request.form['compulsionList'])
    newPlacesList=json.loads(request.form['placeList'])
    newUpload=Upload(newHwsList=newHwsList,newEpisodesList=newEpisodesList, newObsessionsList=newObsessionsList, newTriggersList=newTriggersList, newCompulsionsList=newCompulsionsList, newPlacesList=newPlacesList)
    newUpload.put()

    return "Success"


@app.errorhandler
def pop(error) :
    return error

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('errorPage.html')

@csrf.error_handler
def csrf_error(reason):
    return reason, 400


