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


class Patient(ndb.Model) :
	firstName 		=ndb.StringProperty()
	lastName		=ndb.StringProperty()
	name 			=ndb.StringProperty()
	password		=ndb.StringProperty()
	email 			=ndb.StringProperty()
	uniqueID		=ndb.StringProperty()
	nextAppointment =ndb.StringProperty()
	episodes 		=ndb.IntegerProperty()
	obsessions		=ndb.StringProperty()

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




	
