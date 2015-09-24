#import necessities from flask
from flask import Flask, request, render_template, session, Markup
#import form protection from flaskWTF 
from flask_wtf import Form, CsrfProtect
#import forms
from forms import LoginForm, TherapistRegistrationForm, EnterNoteForm, addERPHWForm
#import auxilliary functions
from auxillaryFunctions import sendEmail, generateCalendar
#import entities for ndb datastore
from entities import Specialist, Manager, Patient, Obsession, Compulsion, Trigger, Note, ERPHW, Place


#general imports
import random, datetime, time,calendar
import string
import json


#temp=Obsession(id='1', obsessionID='1', userID='1', obsession="What if I forgot to lock the door")
#temp.put()
#temp=Obsession(id='2', obsessionID='2', userID='1', obsession="What if I forgot to turn off the stove")
#temp.put()
#temp=Obsession(id='3', obsessionID='3', userID='1', obsession="What if I forgot to lock the window")
#temp.put()
#temp=Obsession(id='4', obsessionID='4', userID='1', obsession="What if I forgot to turn off the lights")
#temp.put()

#temp=Place(placeID="1", patientID='1', place="My kitchen")
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
CsrfProtect(app)
csrf=CsrfProtect()
#set Debug Mode True 
app.config['DEBUG'] = True


# We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

#patient=Patient(firstName="John", name="John Bon", email="JohnBon@mail.com", uniqueID="1", id="1", nextAppointment="9/5/2015", episodes=12)
#patient.put()
#patient=Patient(firstName="Dohn", name="Dohn Bon", email="DohnBon@mail.com", uniqueID="2", id="2", nextAppointment="9/9/2015", episodes=2)
#patient.put()
#patient=Patient(firstName="John", name="John Ban", email="JohnBan@mail.com", uniqueID="3", id="3", nextAppointment="9/7/2015", episodes=8)
#patient.put()
#patient=Patient(firstName="Stan", name="Stan the Man", email="StantheMan@mail.com", uniqueID="4", id="4", nextAppointment="9/8/2015", episodes=3)
#patient.put()

#specialist=Specialist.get_by_id('ecpraterfahey@gmail.com')
#temp=['1','2','3','4']
#specialist.patientCodes=json.dumps(temp)
#specialist.put()

#handle requests to home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test () :
    return render_template('test.html')
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
        return login()
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


#Individual Patients page
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
    session['patientID']=patientCode
    obsessions=Obsession.query(Obsession.userID==patientCode)
    obsessionPills=[]
    obsessionPanes=[]

    triggerList=[]
    obsessionList=[]
    placeList=[]

    isFirst=True
    #generate obsessions and associated triggers and Compulsions tabs
    for obsession in obsessions :
        obsessionList.append((obsession.obsessionID,obsession.obsession))
        if isFirst :
            row='<li class="active"> <a data-toggle="pill" class="nav-pill-gray" href="#'+obsession.obsessionID+'">'
        else :
            row='<li> <a data-toggle="pill" class="nav-pill-gray" href="#'+obsession.obsessionID+'">'
        row+=obsession.obsession+'</a></li>'
        obsessionPills.append(Markup(row))
        #add obsessionPanes
        if isFirst :
            row='<div id="'+obsession.obsessionID+'" class="tab-pane fade in active">'
            isFirst=False
        else :
            row='<div id="'+obsession.obsessionID+'" class="tab-pane fade in">'
        row+='<div class="row"><div class="col-xs-6"><h4 align="center">Triggers</h4>'
        triggers=Trigger.query(Trigger.obsessionID==obsession.obsessionID)
        for trigger in triggers :
            triggerList.append((trigger.triggerID,trigger.trigger))
            row+='<h6>'+trigger.trigger+'</h6>'
        row+='</div> <div class="col-xs-6"><h4 align="center">Compulsions</h4>'
        compulsions=Compulsion.query(Compulsion.obsessionID==obsession.obsessionID)
        for compulsion in compulsions :
            row+='<h6>'+compulsion.compulsion+'</h6>'
        row+='</div></div></div>'
        obsessionPanes.append(Markup(row))
    

    noteForm=EnterNoteForm()
    #generate note pills and panes
    notes=Note.query(Note.patientID==patientCode, Note.specialistID==session['specialistID'])
    notePills=[]
    notePanes=[]
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
        row+="""   
        <div class="btn-toolbar" data-role="editor-toolbar" data-target="#"""+tempID+"""yyeeeeejfdjd">
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
                <a class="btn" data-edit="undo" title="" data-original-title="Undo (Ctrl/Cmd+Z)"><i class="icon-undo"></i></a>
                <a class="btn" data-edit="redo" title="" data-original-title="Redo (Ctrl/Cmd+Y)"><i class="icon-repeat"></i></a>
            </div>
            
        </div>
            <div id=\""""+tempID+'yyeeeeejfdjd" class="noteEditor" contenteditable="true">'+note.note+'</div>'
            #row+=note.note.replace('\n','<br>').replace(' ', '&nbsp')
        row+='</center></div>'

        notePanes.append(Markup(row))



    #generate note list for patient
    noteTitles=[]


    notes=Note.query(Note.patientID==patientCode, Note.specialistID==session['specialistID'])
    for note in notes :
        noteTitles.append(note.noteID)
    currMonth=session['theDate'].month

    places=Place.query(Place.patientID==patientCode)

    for place in places :
        placeList.append((place.placeID, place.place))
    erpHWList=[]
    erpHWs=ERPHW.query(ERPHW.patientID==patientCode)
    for erpHW in erpHWs :
        erpTemp={}
        erpTemp['patientID']=erpHW.patientID
        erpTemp['status']=erpHW.status
        erpTemp['obsession']=erpHW.obsession
        erpTemp['trigger']=erpHW.trigger
        erpTemp['place']=erpHW.place
        erpTemp['prompt']=erpHW.prompt
        erpTemp['time']=erpHW.time
        erpTemp['dateTime']=erpHW.dateTime
        erpHWList.append(erpTemp)
    #generate calendar for patient

    session['triggerList']  =triggerList
    session['obsessionList']=obsessionList
    session['placeList']    =placeList
    session['erpHWList']    =erpHWList

    monthCalendars=generateCalendar(erpHWList, localtime=session['theDate'], obsessions=obsessionList, triggers=triggerList, places=placeList )
    return render_template('patientPage.html', currMonth=currMonth, notePills=notePills, notePanes=notePanes, noteForm=noteForm,noteFormError=None, noteFormSuccess="Success", monthCalendars=monthCalendars, patient=patient, obsessionPills=obsessionPills, obsessionPanes=obsessionPanes)

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
        if specialist.password!=form.password.data :
            return render_template('login.html', form=form, error="Incorrect password")
        if not specialist.emailVerified :
            return render_template('verifyEmail.html')
        session['logged_in']=True
        session['specialistID']=form.email.data
        session['theDate']=datetime.datetime.fromtimestamp(float(form.date.data)/1000.0)
        return myPatients()
    return render_template('login.html', form=form)


# log user out clear session
@app.route('/logout')
def logout() :
    session.clear()
    return home()

#save a note 
@app.route('/saveNote', methods=['GET', 'POST'])
def saveNote() :

    form=EnterNoteForm(request.form)
    if not form.validate() :
        return render_template('newNote.html', noteForm=form, noteFormError="Something went wrong")
    newNote=Note(noteID=form.noteID.data, note=form.note.data,specialistID=session['specialistID'], patientID=session.get('patientID'), dateTime=str(session['theDate']))
    newNote.put()
    theForm=EnterNoteForm()
    return render_template('newNote.html', noteForm=theForm,noteFormError=None, noteFormSuccess="Success")

#get note pane for current patientID
@app.route('/getNotePane')
def getNotePane() :
    #verify logged in
    
    if not session.get('patientID', False) :
        return "error", 400
    #Load patient data
    patient=Patient.get_by_id(session["patientID"])

    if not patient :
        return "error", 400

    #generate note pills and panes
    notes=Note.query(Note.patientID==session['patientID'], Note.specialistID==session['specialistID'])
    notePills=[]
    notePanes=[]
    isFirst=True
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
        row+="""   
        <div class="btn-toolbar" data-role="editor-toolbar" data-target="#"""+tempID+"""yyeeeeejfdjd">
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
        </div>
            <div class="noteEditor" contenteditable="true" id=\""""+tempID+'yyeeeeejfdjd">'+note.note.replace('&nbsp', ' ')+'</div>'
            #row+=note.note.replace('\n','<br>').replace(' ', '&nbsp')
        row+='</center></div>'

        notePanes.append(Markup(row))
    return render_template('notePills.html', notePills=notePills, notePanes=notePanes)


@app.route('/addERPHomework', methods=['POST'])
def addERPHomework() :
    if not session.get('logged_in', False) :
        return render_template('page_not_found.html')
    patientCode=session.get('patientID', False)
    
    if not patientCode :
        return render_template('page_not_found.html')
    form=addERPHWForm(request.form)    


    erpHW=ERPHW(patientID=patientCode, status="Incomplete", obsession= form.obsessions.data, trigger=form.triggers.data, place=form.places.data, prompt=form.prompt.data, time=form.time.data, dateTime=form.localtime.data )
    erpHW.put()
    return viewPatient(patientCode)
    erpTemp={}
    erpTemp['patientID']=erpHW.patientID
    erpTemp['status']=erpHW.status
    erpTemp['obsession']=erpHW.obsession
    erpTemp['trigger']=erpHW.trigger
    erpTemp['place']=erpHW.place
    erpTemp['prompt']=erpHW.prompt
    erpTemp['time']=erpHW.time
    erpTemp['dateTime']=erpHW.dateTime
    session['erpHWList'].append(erpTemp)

    monthCalendars=generateCalendar(erpHWs=session['erpHWList'], localtime=session['theDate'], obsessions=session['obsessionList'], triggers=session['triggerList'], places=session['placeList'] )
    return render_template('calendar.html', monthCalendars=monthCalendars)


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