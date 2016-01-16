from flask import Markup, session, render_template, Markup
import calendar, datetime, json,time, random

from forms import addERPHWForm
#imports for sendgrid 
from sendgrid import SendGridClient
from sendgrid import Mail

from entities import Specialist, Manager, Patient, Obsession, Compulsion, Trigger, Note


def Hasher (name) :
    hashed=""
    for x in name :
        hashed += str(ord(x)*4-3)+':'
    return hashed

def Unhash(hashed) :
    name=""
    hashed=hashed.split(":")
    for x in hashed[:-1] :
        name+=chr((int(x)+3)/4)
    return name


def ERPGraphs(frequencies):
    response={}
    yearChart=""
    yearChart+="function drawERPByYearGraph()" 
    yearChart+="""{

            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Year');
            data.addColumn('number', 'Number of Homeworks');"""

    weekChartFunctions={}
    allWeekChartFunctions={}

    weekDivs=""
    weekChartFunctions=""
    weekChartsToDraw=""

    yearsData="["
    monthChartFunctions={}
    yearChartFunctions=""
    allMonthFunctions=""
    monthChartsToDraw="drawERPByYearGraph();"
    monthChartDivs=""
    selector='<select class="form-control" id="ERPMonthFrequencySelector" style="width:200px;">'                                   
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    isFirst=True
    for year in frequencies :
        registeredMonths={}
        monthChartFunctions={}
        yearsData+="['"+year[:10]+"',"+str(frequencies[year]['number'])+"]," 
        weeks=sorted(frequencies[year])
        minWeek=int(weeks[0])
        maxWeek=int(weeks[len(weeks)-2])
        if maxWeek-minWeek >30 :
            maxWeek=minWeek+4

        #iterate from min week to max week as numbers adding in 0 for each week where not frequencies[year].get(testweekiter,False)
        
        weeks.reverse()

        for week in weeks :
            if week!= 'number' and week!='total' :
                hidden="hidden"
                if isFirst :
                    hidden=""
                weekDivs+='<div '+hidden+' class="erpHWFrequencyGraph" id="ERPHWForWeek'+year+"_"+week+'" style="width:300; height:300"></div>'
                weekChartsToDraw+="drawERPHWForWeekGraph"+year+"_"+week+"();"
                weekChartFunctions+="function drawERPHWForWeekGraph"+year+"_"+week+"() {" 
                weekChartFunctions+="""var data = new google.visualization.DataTable();
                                    data.addColumn('string', 'Day');
                                    data.addColumn('number', 'Number of Homeworks');
                                    data.addRows(["""
                for day in range(0,7) : #frequencies[year][week] :
                    day= str(day)
                    episodesForDay=0
                    if day in frequencies[year][week] : 
                        episodesForDay=frequencies[year][week][day]['number']
                    theDate=datetime.datetime.strptime(year+" "+str(int(week))+" "+day, '%Y %U %w')
                    #secondDate=datetime.datetime.strptime(year+" "+str(int(week)-1)+" 6", '%Y %U %w')
                    weekChartFunctions+='["'+str(theDate.day)+'",'+str(episodesForDay)+"],"

                firstDate=datetime.datetime.strptime(year+" "+str(int(week))+" 0", '%Y %U %w')
                secondDate=datetime.datetime.strptime(year+" "+str(int(week))+" 6", '%Y %U %w')
                secondDateMonth=str(monthDict[secondDate.month])+" "
                if firstDate.month==secondDate.month :
                    secondDateMonth=""
                weekChartFunctions+="""]); var options = {
                                        vAxis: {
                                            title: "Number of HWs",
                                        },
                                        hAxis: {
                                            title: 'Day',
                                        },
                                        legend: 'none',
                                        title: 'ERP HW Frequency """+monthDict[firstDate.month]+" "+str(firstDate.day)+"-"+secondDateMonth+str(secondDate.day)+"""',
                                        };

                                        var chart = new google.visualization.LineChart(document.getElementById('ERPHWForWeek"""+year+"_"+week+"""'));

                                        chart.draw(data, options);
                                        }"""


        for week in range(minWeek,maxWeek+1) :
            
            week=str(week)
            monthChart=""
            monthNum=-3

            if week!='number' :
                monthNum=str(datetime.datetime.strptime(year+" "+week+" 0", '%Y %U %w').month)
                if len(monthNum)==1 :
                    monthNum="0"+monthNum
            tempYear=year
            if not registeredMonths.get(monthNum,False) and monthNum!=-3 and not (int(monthNum)==1 and year=="2015") : 
                hidden=""
                if isFirst :
                    isFirst=False
                else :
                    hidden="hidden"
                registeredMonths[monthNum]=True
                monthChartFunctions[year+str(monthNum)]=""
                monthChartDivs+='<div '+hidden+' class="erpHWFrequencyGraph" id="ERPHWForMonth'+year+"_"+str(monthNum)+'" style="width:300; height:300"></div>'
                monthChartsToDraw+="drawERPHWForMonthGraph"+year+"_"+str(monthNum)+"();"
                monthChartFunctions[year+str(monthNum)]+="function drawERPHWForMonthGraph"+year+"_"+str(monthNum)+"()" 
                monthChartFunctions[year+str(monthNum)]+="""{
                    var data = new google.visualization.DataTable();
                    data.addColumn('string', 'Week');
                    data.addColumn('number', 'Number of Homeworks');"""
                monthChartFunctions[year+str(monthNum)]+="data.addRows(["

            if monthNum!=-3 and  not (int(monthNum)==1 and year=="2015") :
                episodesForThisWeek='0'
                if week in weeks :
                    episodesForThisWeek=str(frequencies[year][week]['number'])
                firstDate=datetime.datetime.strptime(year+" "+str(int(week))+" 0", '%Y %U %w')
                secondDate=datetime.datetime.strptime(year+" "+str(int(week))+" 6", '%Y %U %w')
                secondDateMonth=str(monthDict[secondDate.month])+" "
                if firstDate.month==secondDate.month :
                    secondDateMonth=""
                monthChartFunctions[year+str(monthNum)]+="['"+monthDict[firstDate.month]+" "+str(firstDate.day)+"-"+secondDateMonth+str(secondDate.day)+"',"+episodesForThisWeek+"],"
            
        monthChartFunctionss=sorted(monthChartFunctions)

        for key in monthChartFunctionss :
            if not (int(key[-2:])==1 and year=="2015") :

                monthChartFunctions[key]+="""]); var options = {
                                    vAxis: {
                                        title: "Number of Hws",
                                        },
                                    hAxis: {
                                       title: 'Week',
                                       textStyle: {
        
                                       fontSize: 10,
                                    },
                                    },
                                    
                                   legend: 'none',
                                   title: 'ERP HW Frequency """+monthDict[int(key[-2:])]+" "+year+"""',
                               };

                            var chart = new google.visualization.LineChart(document.getElementById('ERPHWForMonth"""+year+"_"+key[-2:]+"""'));

                            chart.draw(data, options);
                            }"""

                selector+='<option value="ERPHWForMonth'+year+"_"+key[-2:]+'" >Frequencies for '+monthDict[int(key[-2:])]+" "+year+'</option>'
        temp="ddddddddddddddddddddddddddddddddddddddd"        
        for key in monthChartFunctions :
            allMonthFunctions+=monthChartFunctions[key]
    selector+="</select>"
    yearsData+="]"
    yearChart+="data.addRows("+yearsData+");"
    yearChart+= """               var options = {
                    vAxis: {
                        title: "Number of Hws",
                    },
                    hAxis: {
                        title: 'Year',
                    },
                    legend: 'none',
                    title: 'ERPHW Frequency by Year',
                };

            var chart = new google.visualization.LineChart(document.getElementById('ERPByYearGraph'));

            chart.draw(data, options);
            }"""
    yearChartFunctions+=yearChart
    response['weekChartFunctions']=weekChartFunctions
    response['weekDivs']=weekDivs
    response['yearChartFunctions']=yearChartFunctions
    response['monthSelector']=selector
    response['monthChartFunctions']=allMonthFunctions
    response['monthChartsToDraw']=monthChartsToDraw+weekChartsToDraw
    response['monthChartDivs']=monthChartDivs
    return response

def EpisodeGraphs(frequencies):
    response={}
    yearChart=""
    yearChartDivs=""
    yearChart+="function drawEpisodeByYearGraph()" 
    yearChart+="""{

            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Year');
            data.addColumn('number', 'Number of Episodes');"""

    yearChartFunctions=""
    yearsData="["
    monthChartFunctions={}
    allFunctions=""
    monthChartsToDraw=""
    monthChartDivs=""
    selector='<select class="form-control" id="EpisodeMonthFrequencySelector" style="width:200px;">'
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    isFirst=True
    for year in frequencies :
        registeredMonths={}
        monthChartFunctions={}
        yearsData+="['"+year[:10]+"',"+str(frequencies[year]['number'])+"]," 
        weeks=sorted(frequencies[year])

        minWeek=int(weeks[0])
        maxWeek=int(weeks[len(weeks)-2])
        if maxWeek-minWeek >30 :
            maxWeek=minWeek+4

        for week in range(minWeek,maxWeek+1) :
            
            week=str(week)
            monthChart=""
            monthNum=-3
            if week!='number' :
                monthNum=str(datetime.datetime.strptime(year+" "+week+" 0", '%Y %U %w').month)
                if len(monthNum)==1 :
                    monthNum="0"+monthNum
            if not registeredMonths.get(monthNum,False) and monthNum!=-3 and not (int(monthNum)==1 and year=="2015"):
                hidden=""
                if isFirst :
                    isFirst=False
                else :
                    hidden="hidden"
                registeredMonths[monthNum]=True
                monthChartFunctions[year+str(monthNum)]=""
                monthChartDivs+='<div '+hidden+' class="episodeFrequencyGraph" id="EpisodesForMonth'+year+"_"+str(monthNum)+'" style="width:300; height:300"></div>'
                monthChartsToDraw+="drawEpisodesForMonthGraph"+year+"_"+str(monthNum)+"();"
                monthChartFunctions[year+str(monthNum)]+="function drawEpisodesForMonthGraph"+year+"_"+str(monthNum)+"()" 
                monthChartFunctions[year+str(monthNum)]+="""{
                    var data = new google.visualization.DataTable();
                    data.addColumn('string', 'Week');
                    data.addColumn('number', 'Number of Episodes');"""
                monthChartFunctions[year+str(monthNum)]+="data.addRows(["
            if monthNum!=-3 and not (int(monthNum)==1 and year=="2015"):
                episodesForThisWeek='0'
                if week in weeks :
                    episodesForThisWeek=str(frequencies[year][week]['number'])
                firstDate=datetime.datetime.strptime(year+" "+str(int(week))+" 0", '%Y %U %w')
                secondDate=datetime.datetime.strptime(year+" "+str(int(week))+" 6", '%Y %U %w')
                secondDateMonth=str(monthDict[secondDate.month])+" "
                if firstDate.month==secondDate.month :
                    secondDateMonth=""
                monthChartFunctions[year+str(monthNum)]+="['"+monthDict[firstDate.month]+" "+str(firstDate.day)+"-"+secondDateMonth+str(secondDate.day)+"',"+episodesForThisWeek+"],"
        
        monthChartFunctionss=sorted(monthChartFunctions)
        for key in monthChartFunctionss :
            if not (int(key[-2:])==1 and year=="2015") :
                monthChartFunctions[key]+="""]); var options = {
                                    vAxis: {
                                        title: "Number of Episodes",
                                        },
                                    hAxis: {
                                       title: 'Week',
                                       textStyle: {
        
                                       fontSize: 10,
                                    },
                                    },
                                   legend: 'none',
                                   title: 'Episode Frequency """+year+" "+monthDict[int(key[-2:])]+"""',
                               };

                            var chart = new google.visualization.LineChart(document.getElementById('EpisodesForMonth"""+year+"_"+key[-2:]+"""'));

                            chart.draw(data, options);
                            }"""
                selector+='<option value="EpisodesForMonth'+year+"_"+key[-2:]+'" >Frequencies for '+monthDict[int(key[-2:])]+" "+year+'</option>'

        for key in monthChartFunctions :
            allFunctions+=monthChartFunctions[key]
    selector+="</select>"
    yearsData+="]"
    yearChart+="data.addRows("+yearsData+");"
    yearChart+= """               var options = {
                    vAxis: {
                        title: "Number of Episodes",
                    },
                    hAxis: {
                        title: 'Year',
                    },
                    legend: 'none',
                    title: 'Episode Frequency by Year',
                };

            var chart = new google.visualization.LineChart(document.getElementById('EpisodesByYearGraph'));

            chart.draw(data, options);
            }"""
    yearChartFunctions+=yearChart
    response['yearChartFunctions']=yearChartFunctions
    response['yearChartDivs']=yearChartDivs
    response['monthSelector']=selector
    response['monthChartFunctions']=allFunctions
    response['monthChartsToDraw']=monthChartsToDraw
    response['monthChartDivs']=monthChartDivs
    return response


def EpisodeGraphsIntensities(frequencies):
    response={}
    yearChart=""
    yearChart+="function drawEpisodeByYearGraph()" 
    yearChart+="""{

            var data = new google.visualization.DataTable();
            data.addColumn('string', 'Year');
            data.addColumn('number', 'Number of Episodes');"""

    yearChartFunctions=""
    yearsData="["
    monthChartFunctions={}
    allFunctions=""
    monthChartsToDraw=""
    monthChartDivs=""
    selector='<select class="form-control" id="EpisodeMonthFrequencySelector" style="width:200px;">'
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    isFirst=True
    for year in frequencies :
        registeredMonths={}
        monthChartFunctions={}
        yearsData+="['"+year[:10]+"',"+str(frequencies[year]['number'])+"]," 
        weeks=sorted(frequencies[year])
        

        for week in weeks :
            monthChart=""
            monthNum=-3
            if week!='number' :
                monthNum=str(datetime.datetime.strptime(year+" "+week+" 0", '%Y %U %w').month)
            
            if not registeredMonths.get(monthNum,False) and monthNum!=-3 :
                hidden=""
                if isFirst :
                    isFirst=False
                else :
                    hidden="hidden"
                registeredMonths[monthNum]=True
                monthChartFunctions[year+str(monthNum)]=""
                monthChartDivs+='<div '+hidden+' class="episodeFrequencyGraph" id="EpisodesForMonth'+year+"_"+str(monthNum)+'" style="width:300; height:300"></div>'
                monthChartsToDraw+="drawEpisodesForMonthGraph"+year+"_"+str(monthNum)+"();"
                monthChartFunctions[year+str(monthNum)]+="function drawEpisodesForMonthGraph"+year+"_"+str(monthNum)+"()" 
                monthChartFunctions[year+str(monthNum)]+="""{
                    var data = new google.visualization.DataTable();
                    data.addColumn('string', 'Week');
                    data.addColumn('number', 'Number of Episodes');"""
                monthChartFunctions[year+str(monthNum)]+="data.addRows(["
            if monthNum!=-3 :
                avgIntensity='0'
                if week in weeks :
                    avgIntensity=str(frequencies[year][week]['total']/(frequencies[year][week]['number']*1.0))
                firstDate=datetime.datetime.strptime(year+" "+str(int(week)-1)+" 0", '%Y %U %w')
                secondDate=datetime.datetime.strptime(year+" "+str(int(week)-1)+" 6", '%Y %U %w')
                secondDateMonth=str(monthDict[secondDate.month])+" "
                if firstDate.month==secondDate.month :
                    secondDateMonth=""
                monthChartFunctions[year+str(monthNum)]+="['"+monthDict[firstDate.month]+" "+str(firstDate.day)+"-"+secondDateMonth+str(secondDate.day)+"',"+avgIntensity+"],"
            
        for key in monthChartFunctions :
            monthChartFunctions[key]+="""]); var options = {
                                vAxis: {
                                    title: "Number of Episodes",
                                    },
                                hAxis: {
                                   title: 'Week',
                                },
                               legend: 'none',
                               title: 'ERP HW Frequency """+year+" "+monthDict[int(key[-2:])]+"""',
                           };

                        var chart = new google.visualization.LineChart(document.getElementById('EpisodesForMonth"""+year+"_"+key[-2:]+"""'));

                        chart.draw(data, options);
                        }"""
            selector+='<option value="EpisodesForMonth'+year+"_"+key[-2:]+'" >Frequencies for '+monthDict[int(key[-2:])]+" "+year+'</option>'

        for key in monthChartFunctions :
            allFunctions+=monthChartFunctions[key]
    selector+="</select>"
    yearsData+="]"
    yearChart+="data.addRows("+yearsData+");"
    yearChart+= """               var options = {
                    vAxis: {
                        title: "Number of Episodes",
                    },
                    hAxis: {
                        title: 'Year',
                    },
                    legend: 'none',
                    title: 'ERPHW Frequency by Year',
                };

            var chart = new google.visualization.LineChart(document.getElementById('EpisodesByYearGraph'));

            chart.draw(data, options);
            }"""
    yearChartFunctions+=yearChart
    response['yearChartFunctions']=yearChartFunctions
    response['monthSelector']=selector
    response['monthChartFunctions']=allFunctions
    response['monthChartsToDraw']=monthChartsToDraw
    response['monthChartDivs']=monthChartDivs
    return response

def generateTimeCharts (obsessions) :
    
    for obsession in obsessions :
        row="function drawTimeOfDay"+obsession.obsessionID
        row+='''Chart() {
            var data = new google.visualization.DataTable();
            data.addColumn('string', "Time of Day");
            data.addColumn('number', "Episodes");

            data.addRows([

      var options = {
        title: 'Time of Day for Episodes',
        colors: ['#9575cd', '#33ac71'],
        hAxis: {
          title: 'Time of Day',
          format: 'h:mm a',

        },
        vAxis: {
          title: 'Number of Episodes'
        }
      };'''




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
    innerForm+="""<label class="label" for="obsessionSelector">OCD Theme</label>"""
    innerForm+="""<select class="form-control obsessionSelector" id="obsessionSelector" name="obsessions">"""
    #List of triggerSelectors for each obsession
    triggerLists=[]
    placeLists=[]
    for obsessionID,obsession in obsessions :
        newTriggerSelect='<select class="form-control triggerSelector" name="trigger'+obsessionID+":{}:{}{4"+Hasher(obsession)+'" >'
        for triggerID,trigger in triggers[obsessionID] :
            newTriggerSelect+="""<option value=\""""+triggerID+":{}:{}{4"+Hasher(trigger)+'">'+trigger+"""</option>"""
        newTriggerSelect+="</select>"
        triggerLists.append(newTriggerSelect)

        newPlaceSelect='<select class="form-control placeSelector" name="place'+obsessionID+":{}:{}{4"+Hasher(obsession)+'" >'
        for placeID,place in places[obsessionID] :
            newPlaceSelect+=""""<option value=\""""+placeID+":{}:{}{4"+Hasher(place)+'">'+place.replace('"',"&quot;").replace("'","&#39;")+"</option>"""
        newPlaceSelect+="</select>"
        placeLists.append(newPlaceSelect)
        innerForm+="""<option value=\""""+obsessionID+":{}:{}{4"+Hasher(obsession)+'">'+obsession+"""</option>"""
    innerForm+="""</select></div> """

    innerForm+="""<div class="form-group"  align="center">"""
    innerForm+="""<label class="label" for="triggers">Trigger</label>"""
    #innerForm+="""<select class="form-control" id="triggers" name="triggers">"""
    #for triggerID,trigger in triggers :
    #    innerForm+="""<option value=\""""+trigger+'">'+trigger+"""</option>"""
    #innerForm+="""</select></div> """
    for selector in triggerLists :
        innerForm+=selector
    innerForm+="</div> "
    
    innerForm+="""<div hidden class="form-group"  align="center">"""
    innerForm+="""<label class="label" for="places">Places</label>"""
    #innerForm+="""<select class="form-control" id="places" name="places">"""
    #for placeID,place in places :
    #    innerForm+=""""<option value=\""""+place+'">'+place+"</option>"""
    #innerForm+="""</select></div> """
    for selector in placeLists :
        innerForm+=selector
    innerForm+="</div> "
    innerForm+=""" <input hidden id="localtime" name="localtime" type="text" value=\""""+str(datetime)+"""" >"""
    return Markup(innerForm)

def generateERPDisplay(erpHW, theClass, dataTrigger="") :
    anxietyLevel="No Data"
    if erpHW['intensity']!="" :
        anxietyLevel=erpHW['intensity']
    place="No Data"
    if erpHW['place']!="" :
        place=erpHW['place']
    display='<button data-toggle="popover" '+dataTrigger+' data-content="'
    display+="<button class='popoverCloser btn btn-default'>X</button>"
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Time</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+erpHW['time']+'</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Obsession</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+erpHW['obsession']+'</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Trigger</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+erpHW['trigger']+'</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Status</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+erpHW['status']+'</div></div>'                   
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Anxiety Level</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+anxietyLevel+'</div></div>'       
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Time Spent</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+erpHW['resistanceTime']+' Seconds</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Place</strong>:</div></div>'
    display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'>'+place.replace('"',"&quot;").replace("'","&#39;")+'</div></div>'       
    #display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><strong>Prompt</strong>:</div></div>'
    #display+='<div class=\'row\' style=\'min-width:300px\'><div class=\'col-xs-12\'><div contenteditable=\'true\'>'+erpHW['prompt'].replace('"',"'")+'</div></div></div>'
    display+='<button value=\''+erpHW['HWID'].replace('/','-')+'\' class=\'btn removeERPButton\'>Remove HomeWork</button>"'
    if erpHW['status']=="Missed" :
        display+='class="'+theClass+'"><span data-toggle="tooltip" title="Click to view HW Summary"> <i class="fa fa-times-circle-o missed"></i></span></button>'
    elif erpHW['status']=="Incomplete" :
        display+=' class="'+theClass+'"><span data-toggle="tooltip" title="Click to view HW Summary"> <i class="fa fa-circle-o incomplete"></i></span></button>'
    else:
        display+=' class="'+theClass+'"><span data-toggle="tooltip" title="Click to view HW Summary"> <i class="fa fa-check-circle-o complete"></span></i></button>'
    return display


def generateCalendar (erpHWs, localtime, triggers, obsessions, places) :

    cal   = calendar.Calendar(6)
    year  = localtime.year
    theDay=localtime.day
    monthNumber =localtime.month
    #list of all months in years
    allMonths  = cal.yeardatescalendar(year, 1)
    previousYearMonths=cal.yeardatescalendar((year-1), 1)
    nextYearMonths =cal.yeardatescalendar((year+1), 1)
    
    #list of relevant months for calendar
    months = previousYearMonths
    months= months+allMonths
    months= months+ nextYearMonths
    mNumber=monthNumber
    #if monthNumber == 12 :
    #    mNumber=0
    #months+=allMonths[mNumber]

    theMonths=[]
    currMonth=1
    currYear=-1
    isFirst=True
    
    for month in months :
        if currMonth==13 :
            currYear+=1
            currMonth=1
        aMonth='''
        <div '''
        if currMonth==monthNumber and currYear==0 :
            aMonth+='''class="row calendarRow'''
        else :
            aMonth+='''hidden class="row calendarRow'''
        aMonth+=" monthCal"+str(currMonth)+str(currYear)+'''">
        <div class="row"> 
            <div class="col-xs-2">

            </div>
            <div class="col-xs-2" align="center">'''
        if not isFirst : 
            aMonth+='''<a onclick="calNavLeft();" ><span class="glyphicon glyphicon-chevron-left chevy"></span> 
                </a>'''
        isFirst=False
        aMonth+='''</div>
            <div class="col-xs-4" align="center">'''
        aMonth+=calendar.month_name[currMonth]
        aMonth+='''</div>
            <div class="col-xs-2" align="center">'''
        if currMonth==12 and currYear==2 :
            pass
        else :
            aMonth+='''<a onclick="calNavRight();" ><span class="glyphicon glyphicon-chevron-right chevy"></span> 
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
        for week in month[0] :
            aMonth+='<tr>'
            for day in week :
                if day.month==currMonth :
                    aMonth+='<td class="day currMonthDay">'
                else :
                    aMonth+='<td class="day notCurrMonthDay">'
                
                if ((monthNumber-day.month)>0 and not currYear==1) or currYear==-1 or (currYear==0 and day.month==12 and (currMonth!=monthNumber)) :
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
                aMonth+='<div class="HWContainer"><center>'
                for erpHW in erpHWs :
                    if erpHW['dateTime'][:10].replace('/','-')==str(day) :
                        aMonth+=generateERPDisplay(erpHW)
                aMonth+='</center></div>'
                aMonth+='</td>'
            aMonth+='</tr>'
        aMonth+='</table> </div> </div> </div>'
        currMonth+=1
        theMonths.append(Markup(aMonth))
    return theMonths
def generateCalendars (erpHWs, localtime, triggers, obsessions, places) :

    cal   = calendar.Calendar(6)
    year  = localtime.year
    theDay=localtime.day
    monthNumber =localtime.month
    #list of all months in years
    allMonths  = cal.yeardatescalendar(year, 1)
    previousYearMonths=cal.yeardatescalendar((year-1), 1)
    nextYearMonths =cal.yeardatescalendar((year+1), 1)
    
    #list of relevant months for calendar
    months = previousYearMonths[8:]
    months= months+allMonths[:8]
    #months=allMonths
    #months= months+ nextYearMonths
    mNumber=monthNumber
    #if monthNumber == 12 :
    #    mNumber=0
    #months+=allMonths[mNumber]
    finalYear=0
    finalMonth=8
    theMonths=[]
    currMonth=9
    currYear=-1
    isFirst=True
    
    for month in months :
        if currMonth==13 :
            currYear+=1
            currMonth=1
        aMonth='''
        <div '''
        if currMonth==monthNumber and currYear==0 :
            aMonth+='''class="row calendarRow'''
        else :
            aMonth+='''hidden class="row calendarRow'''
        aMonth+=" monthCal"+str(currMonth)+str(currYear)+'''">
        <div class="row"> 
            <div class="col-xs-2">

            </div>
            <div class="col-xs-2" align="center">'''
        if not isFirst : 
            aMonth+='''<a onclick="calNavLeft();" ><span class="glyphicon glyphicon-chevron-left chevy"></span> 
                </a>'''
        isFirst=False
        aMonth+='''</div>
            <div class="col-xs-4" align="center">'''
        aMonth+=calendar.month_name[currMonth]+' '+str(year+currYear)
        aMonth+='''</div>
            <div class="col-xs-2" align="center">'''
        if currMonth==finalMonth and currYear==finalYear :
            pass
        else :
            aMonth+='''<a onclick="calNavRight();" ><span class="glyphicon glyphicon-chevron-right chevy"></span> 
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
        for week in month[0] :
            aMonth+='<tr>'
            for day in week :
                isCurr=False
                if day.month==currMonth :
                    isCurr=True
                    aMonth+='<td class="day currMonthDay">'
                else :
                    isCurr==False
                    aMonth+='<td class="day notCurrMonthDay">'
                aMonth+="<div class='container-fluid dayContainer' ><div class='row'><div class='col-xs-12 dayCol'>"
                if ((monthNumber-day.month)>0 and not currYear==1) or currYear==-1 or (currYear==0 and day.month==12 and (currMonth!=monthNumber)) :
                    pass
                elif (monthNumber-day.month)==0 : 
                    if day.day>=theDay :
                        innerForm=erpForm(obsessions,places, triggers, day)
                        addForm=addERPHWForm()
                        aMonth+='<button class="addERPButton '+str(day.month)+' '+str(currMonth) +' pop" data-toggle="popovers" data-content=\''+render_template('erpHWForm.html', form=addForm, innerForm=innerForm)+'\'> <span data-toggle="tooltip" title="Click to add HW" class="glyphicon glyphicon-plus glyph-blue"></span></button>'
                elif isNextMonth(day.month, currMonth) or (day.month>monthNumber and day.year>=year) or day.year>=year : 
                    innerForm=erpForm(obsessions,places, triggers, day)
                    addForm=addERPHWForm()
                    aMonth+='<button class="addERPButton '+str(day.month)+' '+str(currMonth)+'" data-toggle="popovers" data-content=\''+render_template('erpHWForm.html', form=addForm, innerForm=innerForm)+'\'> <span data-toggle="tooltip" title="Click to add HW" class="glyphicon glyphicon-plus glyph-blue"></span></button>'
                aMonth+='<span class="dayDate">'+str(day.day)+'</span>'
                aMonth+='</div></div>'
                #Should be handling events right now placing random
                if erpHWs.get(day, False) :
                    if len(erpHWs[day]) >3 :
                        aMonth+="<div class='row'><div class='col-xs-12'><center>"
                        aMonth+='<button type ="button" class="btn btn-default showHWButton" data-toggle="collapse" data-target="#HWs'+str(day)+str(isCurr)+'"><span data-toggle="tooltip" title="Click to Expand HW\'s">HWs</span></button>'
                        aMonth+="<div class='hwContainer collapse' id='HWs"+str(day)+str(isCurr)+"'>"
                        for erpHW in erpHWs[day] :
                            #aMonth+='<li>'
                            #aMonth+=generateERPDisplay(erpHW, "ERPHWLi",   'data-trigger="hover;"')
                            #aMonth+='</li>'
                        #aMonth+='</ul></div>' 
                            aMonth+=generateERPDisplay(erpHW,"ERPHWSmall", )
                        aMonth+="</div>"
                    else :
                        aMonth+="<div class='row hwRow'><div class='col-xs-12'><center>"
                        for erpHW in erpHWs[day] :
                            aMonth+=generateERPDisplay(erpHW,"ERPHWButton",)

                aMonth+='</center>'
                aMonth+='</div></div>'
                aMonth+="</div>"
                aMonth+='</td>'
            aMonth+='</tr>'
        aMonth+='</table> </div> </div> </div>'
        currMonth+=1
        theMonths.append(Markup(aMonth))
    return theMonths




def isNextMonth(testMonth, currMonth) :
    if currMonth+1==testMonth :
        return True
    return currMonth==12 and testMonth==1



