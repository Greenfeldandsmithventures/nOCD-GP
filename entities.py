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


class Patient(ndb.Model) :
	name 			=ndb.StringProperty()
	password		=ndb.StringProperty()
	email 			=ndb.StringProperty()
	uniqueID		=ndb.StringProperty()
	nextAppointment =ndb.StringProperty()
	episodes 		=ndb.IntegerProperty()



	
