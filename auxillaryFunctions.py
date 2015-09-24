from flask import Markup, session, render_template, Markup
import calendar, datetime, json,time, random

from forms import addERPHWForm
#imports for sendgrid 
from sendgrid import SendGridClient
from sendgrid import Mail

from entities import Specialist, Manager, Patient, Obsession, Compulsion, Trigger, Note


def sendEmail(sender, recipient, subject, html, text) :
    sg= SendGridClient('ecpf', 'Iheart1!', secure=True)
    message = Mail()
    message.set_subject(subject)
    message.set_html(html)
    message.set_text(text)
    message.set_from(sender)
    message.add_to(recipient)
    sg.send(message)
    return True


def erpForm(obsessions, places, triggers, datetime) :
    innerForm='''<div class="form-group"  align="center">'''
    innerForm+="""<label class="label" for="obsessions">OCD Theme</label>"""
    innerForm+="""<select class="form-control" id="obsessions" name="obsessions">"""
    for obsessionID,obsession in obsessions :
        innerForm+="""<option value=\""""+obsession+'">'+obsession+"""</option>"""
    innerForm+="""</select></div> """

    innerForm+="""<div class="form-group"  align="center">"""
    innerForm+="""<label class="label" for="triggers">Trigger</label>"""
    innerForm+="""<select class="form-control" id="triggers" name="triggers">"""
    for triggerID,trigger in triggers :
        innerForm+="""<option value=\""""+trigger+'">'+trigger+"""</option>"""
    innerForm+="""</select></div> """
    

    innerForm+="""<div class="form-group"  align="center">"""
    innerForm+="""<label class="label" for="places">Places</label>"""
    innerForm+="""<select class="form-control" id="places" name="places">"""
    for placeID,place in places :
        innerForm+=""""<option value=\""""+place+'">'+place+"</option>"""
    innerForm+="""</select></div> """
    innerForm+=""" <input hidden id="localtime" name="localtime" type="text" value=\""""+str(datetime)+"""" >"""
    return Markup(innerForm)

def generateCalendar (erpHWs, localtime, triggers, obsessions, places) :

    cal   = calendar.Calendar(6)
    year  = localtime.year
    theDay=localtime.day
    monthNumber =localtime.month
    #list of all months in years
    allMonths  = cal.yeardatescalendar(year, 1)
    #list of relevant months for calendar
    months = []
    months+=allMonths[monthNumber-2]
    months+=allMonths[monthNumber-1]
    months+=allMonths[monthNumber]

    theMonths=[]
    currMonth=monthNumber-1
    isFirst=True
    for month in months :
        aMonth='''
        <div '''
        if currMonth==monthNumber :
            aMonth+='''class="row calendarRow'''
        else :
            aMonth+='''hidden class="row calendarRow'''
        aMonth+=" monthCal"+str(currMonth)+'''">
        <div class="row"> 
            <div class="col-xs-2">

            </div>
            <div class="col-xs-2" align="center">'''
        if not isFirst : 
            aMonth+='''<a onclick="calNavLeft();" ><span class="glyphicon glyphicon-chevron-left"></span> 
                </a>'''
        isFirst=False
        aMonth+='''</div>
            <div class="col-xs-4" align="center">'''
        aMonth+=calendar.month_name[currMonth]
        aMonth+='''</div>
            <div class="col-xs-2" align="center">'''
        if currMonth==monthNumber+1 :
            pass
        else :
            aMonth+='''<a onclick="calNavRight();" ><span class="glyphicon glyphicon-chevron-right"></span> 
                </a>'''
        aMonth+='''
            </div>

            <div class="col-xs-2">


            </div>

        </div>
        <div class="row"> 
            <div class="col-xs-12">
        
        <table class="table-bordered '''
        aMonth+=" month"+str(currMonth)
        aMonth+='''">
        <thead>  <!--Header row for the Table-->
            <th class="dayHeader "> <center>Sunday    </center></th>
            <th class="dayHeader "> <center> Monday   </center></th>
            <th class="dayHeader "> <center> Tuesday  </center></th>
            <th class="dayHeader "> <center>Wednesday </center></th>
            <th class="dayHeader "> <center>Thursday  </center></th>
            <th class="dayHeader "> <center>Friday    </center></th>
            <th class="dayHeader "> <center>Saturday  </center></th>
        </thead>
        '''
        for week in month :
            aMonth+='<tr>'
            for day in week :
                if day.month==currMonth :
                    aMonth+='<td class="day currMonthDay">'
                else :
                    aMonth+='<td class="day notCurrMonthDay">'
                
                if (monthNumber-day.month)>0 :
                    pass
                elif (monthNumber-day.month)==0 : 
                    if day.day>=theDay :
                        innerForm=erpForm(obsessions,places, triggers, day)
                        addForm=addERPHWForm()
                        aMonth+='<button class="addERPButton" data-toggle="popovers" data-content=\''+render_template('erpHWForm.html', form=addForm, innerForm=innerForm)+'\'> <span class="glyphicon glyphicon-plus glyph-blue"></span></button>'
                else : 
                    innerForm=erpForm(obsessions,places, triggers, day)
                    addForm=addERPHWForm()
                    aMonth+='<button class="addERPButton" data-toggle="popovers" data-content=\''+render_template('erpHWForm.html', form=addForm, innerForm=innerForm)+'\'> <span class="glyphicon glyphicon-plus glyph-blue"></span></button>'
                aMonth+='<span class="dayDate">'+str(day.day)+'</span>'
                #Should be handling events right now placing random
                aMonth+='<center>'
                for erpHW in erpHWs :
                    if erpHW['dateTime'][:11]==str(day) :                   
                        if erpHW['status']=="Missed" :
                            aMonth+='<button data-toggle="popover" data-content="<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'>'+erpHW['time']+'</div><div class=\'col-xs-10\'>Obsession:'+erpHW['obsession']+'</div></div><div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'></div><div class=\'col-xs-10\'>Trigger:'+erpHW['trigger']+'</div></div><div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'></div><div class=\'col-xs-10\'>Status:'+erpHW['status']+'</div></div>" class="ERPHWButton"><i class="fa fa-times-circle-o missed"></i></button>'
                        elif erpHW['status']=="Incomplete" :
                            aMonth+='<button data-toggle="popover" data-content="<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'>'+erpHW['time']+'</div><div class=\'col-xs-10\'>Obsession:'+erpHW['obsession']+'</div></div><div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'></div><div class=\'col-xs-10\'>Trigger:'+erpHW['trigger']+'</div></div><div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'></div><div class=\'col-xs-10\'>Status:'+erpHW['status']+'</div></div>" class="ERPHWButton"><i class="fa fa-circle-o incomplete"></i></button>'
                        else:
                            aMonth+='<button data-toggle="popover" data-content="<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'>'+erpHW['time']+'</div><div class=\'col-xs-10\'>Obsession:'+erpHW['obsession']+'</div></div><div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'></div><div class=\'col-xs-10\'>Trigger:'+erpHW['trigger']+'</div></div><div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-2\'></div><div class=\'col-xs-10\'>Status:'+erpHW['status']+'</div></div>" class="ERPHWButton"><i class="fa fa-check-circle-o complete"></i></button>'
                aMonth+='</center>'
                aMonth+='</td>'
            aMonth+='</tr>'
        aMonth+='</table> </div> </div> </div>'
        currMonth+=1
        theMonths.append(Markup(aMonth))
    return theMonths
