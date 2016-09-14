# Mailinator API handler class for Jostle Corporation QA

__author__ = "Kimar Neves"
__version__ = "1.0"

import time
import json
import string
#import requests
import datetime
from get_datetime import get_datetime   #date\time funtion that we use for file names

from writer import writer       	        #function to handle outputs
from email.Utils import formatdate

class mailinatorApi:
	"""this class is to be used API calls to Jostle's Insightly CRM database """

	def __init__(self):
		"""Initializes the Mailinator API object"""
		self.baseURL = "https://mailinator.com/api/"
		self.output = []
		self.counter = 0

	def mailinatorApiCall(self, recipient):
		"""makes a REST API call to mailgun to get the events for a certain person
		   from the time of the call to 'end' (looks back in time)"""
		urlToCheck = self.baseURL+"webinbox?to="+recipient.split('@')[0]#+"&token=..." 
		print urlToCheck

		data = requests.get(urlToCheck,verify=True)
		print data
		eventLib = json.loads(data.text)
		return eventLib 

	def typeChecks(self, recipient, sentSubject, emailSent):
		"""checks that the 'recipient' is either a string or a list of stringsand checks 
		that the subject is a string"""
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

	def timePast(self,now,end):
		"""calculates time past since the start of the test"""
		startDate = datetime.datetime.strptime(end,"%Y.%m.%d_%H.%M.%S.%f")
		endDate = datetime.datetime.strptime(now[0],"%Y.%m.%d_%H.%M.%S.%f")
		return (endDate-startDate).total_seconds()

	def subjectChecking(self, recipient, sentSubject, end):
		"""checks that the sentSubject is the same as the recievedSubject """
		# Implements a loop for checking e-mail was received using intervals of 30 seconds.
		attempts = 0
		# self.output = writer("INFO:\tFound email with correct subject", self.output)
		while attempts < 10:#Loop through mail checking, allowing 10 checking done in a 5 minutes period.
			found = False
			eventLib = self.mailinatorApiCall(recipient)
			writer("INFO:\tAPI: " + self.baseURL, self.output)
			self.output = writer("INFO:\tAttempt " + str(attempts+1), self.output)
			now = get_datetime()
			timePast = self.timePast(now,end)
			self.output = writer("INFO sentSubject:\t " + sentSubject, self.output)
			print eventLib
			# self.output = writer("INFO:\tResponse: " + str(eventLib), self.output)#For DEBUG
			for i in range(len(eventLib["messages"])):
				emailSubject = eventLib["messages"][i]["subject"]
				timePastEmail = eventLib["messages"][i]["seconds_ago"]
				# self.output = writer("INFO emailSubject:\t " + emailSubject, self.output)
				if (sentSubject == emailSubject and timePast > timePastEmail):
					result = "Match"
					found = True
					self.output = writer("INFO:\tFound email with correct subject", self.output)
					msgIdToDelete = eventLib["messages"][i]["id"]
					self.output = writer("INFO:\tFound email with correct subject ID: "+msgIdToDelete, self.output)
					#Delete e-mail that was created by test
					time.sleep(1)
					urlToDelete = "https://mailinator.com/api/expunge?msgid="+msgIdToDelete
					requests.get(urlToDelete,verify=True)
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

	def emailVerification(self, recipient, sentSubject, end, emailSent):
		"""accepts recipient (string or list of strings): email recipients,
                   sentSubject (string) : email subject to find,
                   end (date time string): to set the lookback window
                   emailSent (True or False): stating whether or not the email was expected to be sent"""
		recipient, sentSubject, emailSent = self.typeChecks(recipient, sentSubject, emailSent)    #checking valid types
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
	output = ["header", "line 1"]
	checkEmails = mailinatorApi()
	logins = "ryanhoward_usqa@mailinator.com"
	subject = "Jim, you have just been made a TEAMS Administrator in ApplesRus "
	end = "2015.10.29_17.48.07.691487"
	checkEmails.emailVerification(recipient=logins, sentSubject=subject, end=end, emailSent=True)
	# for entry in checkEmails.output:
	# 	output.append(entry)

	# print checkEmails.counter













