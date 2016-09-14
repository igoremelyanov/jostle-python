# Mailgun API class for Jostle Corporation QA

__author__ = "Jeremy Erickson"
__version__ = "1.0"

import time
import json
import string
import requests
import datetime

from writer import writer       	        #function to handle outputs
from email.Utils import formatdate

class jostleMailgun:
	"""this class is to be used API calls to Jostle's Insightly CRM database """

	def __init__(self, source):
		"""Initializes the Mailgun API object"""
		self.baseURL =  ""
		if(source == "qa-email.jostletest.com"):
			self.baseURL = "https://api.mailgun.net/v2/qa-email.jostletest.com/events"
		else:
			self.baseURL = "https://api.mailgun.net/v2/jostletest1.mailgun.org/events"
		self.user = "api"
		self.key = "key-4e1cbe9tvp6mcxhap7jeytsjdrkox7w0"
		self.output = []
		self.counter = 0

	def mailgunCall(self, recipient, end):
		"""makes a REST API call to mailgun to get the events for a certain person
		   from the time of the call to 'end' (looks back in time)"""
		print "Recipient: "+recipient
		data = requests.get(self.baseURL,
							auth=(self.user,self.key),
							params = {
									  "ascending" : "no",
									   "end" : end,
									   #"to" : recipient  # JOS-6821 - Aut Regression is failing on emails
									   #For some reason our api call to mailgun will not return any results when recipient or to is used as a param, 
									   # the hack/work around is to suck back all the emails and filter them by 'to" in subject checking'

									 })
		eventLib = json.loads(data.text)
		#print eventLib
		return eventLib

	def switchToMailgunDomain(self, recipient, source):
		"""changes the @_______ to @qa-email.jostletest.com"""
 		if isinstance(recipient,str):
			# This determines the mail server in use
 			if(source == "qa-email.jostletest.com"):
				recipient = recipient.split("@")[0] + "@qa-email.jostletest.com"
			else:
				recipient = recipient.split("@")[0] + "@jostletest1.mailgun.org"
		elif isinstance(recipient,list):
			for i,entry in enumerate(recipient):
				# This determines the mail server in use
				if(source == "qa-email.jostletest.com"):
					recipient[i] = recipient[i].split("@")[0] + "@qa-email.jostletest.com"
				else:
					recipient[i] = recipient[i].split("@")[0] +  "@jostletest1.mailgun.org"
		return recipient

	def convertToRFC2822(self, end):
		""" converts a date string with the format, for example, 2014.03.05_12.35.01.750000
		    into RFC2822 format required for the mailgun api call"""
		dt_Obj = datetime.datetime.strptime(end,"%Y.%m.%d_%H.%M.%S.%f") #- datetime.timedelta(minutes=90) # this is a hack to set the date back a couple of minutes to give a bigger search window.
		dt_RFC = formatdate(time.mktime(dt_Obj.timetuple()))
		return dt_RFC

	def typeChecks(self, recipient, sentSubject, emailSent):
		"""checks that the 'recipient' is either a string or a list of strings
       		and checks that the subject is a string"""
		if not isinstance(sentSubject,str):
			raise ValueError("emailVerification() requires string as second argument")
		if not isinstance(recipient,str) and not isinstance(recipient,list):
			raise ValueError("emailVerification() accepts string or list of strings as first argument")
		if isinstance(recipient,list):
  			stringCheck = [isinstance(entry,str) for entry in recipient]
			if False in stringCheck:
				raise ValueError("one of the entries in the 'recipient' list is not a string")
		if emailSent != True and emailSent != False:
			raise ValueError("emailVerification() accepts True or False as argument for 'emailSent'")
		return recipient, sentSubject, emailSent

	def subjectChecking(self, recipient, sentSubject, end):
		"""checks that the sentSubject is the same as the recievedSubject """
		# Implements a loop for checking e-mail was received using intervals of 30 seconds.
		attempts = 0
		# self.output = writer("INFO:\tFound email with correct subject", self.output)
		while attempts < 10:#Loop through mail checking, allowing 10 checking done in a 5 minutes period.
			found = False
			eventLib = self.mailgunCall(recipient, end)
			writer("INFO:\tAPI: " + self.baseURL, self.output)
			self.output = writer("INFO:\tAttempt " + str(attempts+1), self.output)
			# Check this - self.output = writer("INFO:\emails " + str(en(eventLib["items"])), self.output)
			for i in range(len(eventLib["items"])):
				emailSubject = eventLib["items"][i]["message"]["headers"]["subject"]
				# JOS-6821 - Aut Regression is failing on emails - remove the next line when emails are filtered correctly
				emailTo = eventLib["items"][i]["message"]["headers"]["to"] # added this as a hack because we did not filter by recipient in the previous call to solve JOS-6821
				#emailRecipient = eventLib["items"][i]["recipient"]
				self.output = writer("INFO sentSubject:\t " + sentSubject, self.output)
				self.output = writer("INFO emailSubject:\t " + emailSubject, self.output)
				self.output = writer("INFO emailTo:\t " + emailTo, self.output) # 
				#self.output = writer("INFO emailRecipient:\t " + emailRecipient, self.output)
				if sentSubject == emailSubject and emailTo == recipient: # added the check for emailTo because we did not filter the emails earlier remove the AND emailTo after mailgun filters by recipient again JOS-6821
					result = "Match"
					found = True
					self.output = writer("INFO:\tFound email with correct subject & recipient", self.output)
					break
				else:pass
			if found:
				break#exit in case mail is found.
			time.sleep(30)#allow a delay in order to wait e-mail arrive in server
			# self.output = writer("INFO:\tFound email with correct subject", self.output)
			attempts+=1

		if attempts >= 10:
			result = "No Match"
			self.output = writer("INFO:\tNo email found with desired subject", self.output)
		return result

	def emailIsExpected(self, recipient, sentSubject, end):
		"""checking to whether an email that was expected to arrive was present """
		self.output = writer("INFO:\tExpecting to find email for "+ recipient, self.output)
		self.output = writer("INFO:\tSearching for email...." + sentSubject, self.output)
		result = self.subjectChecking(recipient, sentSubject, end)
		if result == "Match":
			self.output = writer("VERIFY:\tEmail WAS expected and IS present\tPASS", self.output)
			self.counter += 1
		if result == "No Match":
			self.output = writer("VERIFY:\tEmail WAS expected and is NOT present\tFAIL", self.output)

	def emailNotExpected(self, recipient, sentSubject, end):
		"""checking to see whether an email that was not expected to arrive was absent"""
		self.output = writer("INFO:\tNot expecting to find email for "+ recipient, self.output)
		self.output = writer("INFO:\tSearching for email....", self.output)
		result = self.subjectChecking(recipient, sentSubject, end)
		if result == "Match":
			self.output = writer("VERIFY:\tEmail was NOT expected and IS present\tFAIL", self.output)
		if result == "No Match":
			self.output = writer("VERIFY:\tEmail was NOT expected and is NOT present\tPASS", self.output)
			self.counter += 1

	def emailVerification(self, recipient, sentSubject, source, end, emailSent):
		"""accepts recipient (string or list of strings): email recipients,
                   sentSubject (string) : email subject to find,
                   end (date time string): to set the lookback window
                   emailSent (True or False): stating whether or not the email was expected to be sent"""
		recipient, sentSubject, emailSent = self.typeChecks(recipient, sentSubject, emailSent)    #checking valid types
		end = self.convertToRFC2822(end)														  #converting date to RFC 2822
		recipient = self.switchToMailgunDomain(recipient, source)                   					  #switch email domain to mailgun
		if isinstance(recipient,str):
			if emailSent == True:
				self.emailIsExpected(recipient, sentSubject, end)
			if emailSent == False:
				self.emailNotExpected(recipient, sentSubject, end)
		if isinstance(recipient, list):
			if emailSent == True:
				for person in recipient:
					self.emailIsExpected(person, sentSubject, end)
			if emailSent == False:
				for person in recipient:
					self.emailNotExpected(person, sentSubject, end)

if __name__ == "__main__":
	end = "2014.03.05_12.35.01.750000"
	output = ["header", "line 1"]
	logins = ["jasonjones@mailinator.com","michaelgaryscott@mailinator.com"]
	subject = "sent on wednesday"
	checkEmails = jostleMailgun("jostletest1.mailgun.org")
 	checkEmails.emailVerification(recipient=logins, sentSubject=subject, source="jostletest1.mailgun.org", end=end, emailSent=True)
	#checkEmails.emailVerification(1, subject, end)
	#checkEmails.emailVerification("jason@mailinator.com", subject, end, emailSent=True)
	for entry in checkEmails.output:
		output.append(entry)

	print checkEmails.counter













