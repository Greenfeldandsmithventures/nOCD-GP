from google.appengine.ext import ndb
import cgi

class Manager(ndb.Model):
	username=ndb.StringProperty()
	password=ndb.StringProperty()

	@classmethod
	def query_managers(cls,ancestor_key):
		return cls.query(ancestor=ancestor_key)

#Class for the specialist 
#Invitations are stored as seperate models linked by specialist 

class Errorr(ndb.Model) :
	error=ndb.StringProperty()

class Specialist(ndb.Model) :
	name           	=ndb.StringProperty()
	email          	=ndb.StringProperty()
	password   	   	=ndb.StringProperty()
	nameOfPractice 	=ndb.StringProperty()
	address			=ndb.StringProperty()
	city			=ndb.StringProperty()
	state			=ndb.StringProperty()
	country			=ndb.StringProperty()
	verified		=ndb.BooleanProperty()
	emailVerified   =ndb.BooleanProperty()
	typesOfPractice =ndb.StringProperty()
	patientCodes	=ndb.StringProperty()
	secretCode		=ndb.StringProperty()
	numberRequests	=ndb.IntegerProperty()


class Patient(ndb.Model) :
	firstName 		=ndb.StringProperty()
	lastName		=ndb.StringProperty()
	name 			=ndb.StringProperty()
	password		=ndb.StringProperty()
	email 			=ndb.StringProperty()
	uniqueID		=ndb.StringProperty()
	lastAppointment =ndb.StringProperty()
	nextAppointment =ndb.StringProperty()
	episodes 		=ndb.IntegerProperty()
	resistanceTime	=ndb.IntegerProperty()


class Trigger(ndb.Model) :
	triggerID		=ndb.StringProperty()
	obsessionID		=ndb.StringProperty()
	trigger 		=ndb.StringProperty()
	userID			=ndb.StringProperty()

class Interests(ndb.Model) :
	interestID		=ndb.StringProperty()
	userID			=ndb.StringProperty()
	interest 		=ndb.StringProperty()

class Obsession(ndb.Model) :
	obsessionID		=ndb.StringProperty()
	userID			=ndb.StringProperty()
	obsession 		=ndb.StringProperty()

class Tasks(ndb.Model) :
	taskID			=ndb.StringProperty()
	userID			=ndb.StringProperty()
	task 			=ndb.StringProperty()

class Hobbies(ndb.Model) :
	hobbyID 		=ndb.StringProperty()
	userID 			=ndb.StringProperty()
	hobby 			=ndb.StringProperty()

class Compulsion(ndb.Model) :
	compulsionID	=ndb.StringProperty()
	obsessionID		=ndb.StringProperty()
	compulsion 		=ndb.StringProperty()
	userID			=ndb.StringProperty()

class Place(ndb.Model) :
	placeID			=ndb.StringProperty()
	userID			=ndb.StringProperty()
	latitude		=ndb.StringProperty()
	longitude		=ndb.StringProperty()
	place 			=ndb.StringProperty()
	obsessionID		=ndb.StringProperty()


class ERPHW(ndb.Model) :
	HWID			=ndb.StringProperty()
	userID			=ndb.StringProperty()
	status			=ndb.StringProperty()
	obsession		=ndb.StringProperty()
	obsessionID		=ndb.StringProperty()
	triggerID		=ndb.StringProperty()
	trigger			=ndb.StringProperty()
	place			=ndb.StringProperty()
	intensity		=ndb.StringProperty()
	prompt			=ndb.TextProperty()
	resistanceTime	=ndb.StringProperty()
	time 			=ndb.StringProperty()
	dateTime		=ndb.StringProperty()
	new				=ndb.BooleanProperty()

class Episode(ndb.Model) :
	episodeID	    =ndb.StringProperty()
	latitude		=ndb.FloatProperty()
	longitude		=ndb.FloatProperty()
	userID			=ndb.StringProperty()
	obsession		=ndb.StringProperty()
	obsessionID		=ndb.StringProperty()
	triggerID		=ndb.StringProperty()
	trigger			=ndb.StringProperty()
	compulsion 		=ndb.StringProperty()
	compulsionID	=ndb.StringProperty()
	place			=ndb.StringProperty()
	resistanceTime	=ndb.StringProperty()
	time 			=ndb.StringProperty()
	dateTime		=ndb.StringProperty()
	intensity 		=ndb.IntegerProperty()
	heartRate		=ndb.IntegerProperty()

class Note(ndb.Model) :
	noteID			=ndb.StringProperty()
	dateTime		=ndb.StringProperty()
	note 			=ndb.TextProperty()
	specialistID	=ndb.StringProperty()
	userID			=ndb.StringProperty()

class Request(ndb.Model) :
	patientName		=ndb.StringProperty()
	userID			=ndb.StringProperty()
	specialistID	=ndb.StringProperty()
	message			=ndb.TextProperty()

class Upload(ndb.Model) :
	newHwsList			=ndb.TextProperty()
	newEpisodesList		=ndb.TextProperty()
	newObsessionsList	=ndb.TextProperty()    
	newTriggersList		=ndb.TextProperty()
	newCompulsionsList	=ndb.TextProperty()
	newPlacesList		=ndb.TextProperty()

	
