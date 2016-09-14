# class that can be used to check Jostle Mailinator Email Testing Account

import requests
import json
import time
from datetime import datetime

__author__ = "Jeremy Erickson" #<jeremy@jostle.me>
__version__= "1.0.0"


class jostleMailinator:
	"""This class is to be used for email testing etc.
		with the Jostle Mailinator Account """

	def __init__(self):
		"""Initializes the mailinator object. Gives the username
			and password along with the API Token """
		self.username = "Ship1Stop2"
		self.password = "119WestPender"
		self.eDomain = "Ship1Stop2@mailinatorpro.com"
		self.token = "4713527f3ab04590b3406f581f434887"     #the API Token. Found in Settings on MailPro


	def getEmail(self):
		"""gets all the email in the box for Ship1Stop2@mailinatorpro.com
			and returns a list containing libraries of information for each message """
		resp = requests.get("https://api.mailinatorpro.com/api/inbox?&access_token="+self.token)
		allEmail = json.loads(resp.text)    #returns a library with msglist,stats and api_version
		if allEmail["msglist"] == []:
			print "This inbox is empty"
			return None
		else:
			self.msgList = allEmail['msglist']  #getting only the message list
			return self.msgList


	def emailsVerify(self, emails, status, subject, time, window=100):
		"""This function checks for the PRESENCE or ABSENCE of an email in a bunch of inboxes
			it takes a list of logins and checks the entire inbox for emails sent to that person
			of those emails it checks the subject for a match to the desired subject
			#time is the approximate time the email was sent (in Linux time)
			#window is the time tolerance for the email to be a match """
		self.counter = 0    #pass counter
		self.results = []    #for result outputs
		self.time = float(time)
		self.window = float(window)
		self.timePlus = int(self.time + self.window) 	#sets upper bound
		self.timeMinus = int(self.time - self.window)    #sets lower bound
		allEmails = jostleMailinator.getEmail(self)
		for j,entry in enumerate(emails):
			emails[j] = entry.lower()       #takes any uppercase and makes it lower so mailinator understands
		if allEmails != None:
			for account in emails:
				print "INFO:\tLooking for emails sent to "+ str(account)
				self.results.append("INFO:\tLooking for emails to "+ str(account)+"\n")
				for lib in allEmails:
					emailTime = int(str(lib["time"])[:-3])
					if account == lib["to"]:
						if subject == lib["subject"] and (emailTime<self.timePlus and emailTime>self.timeMinus):
							if status == "Present":   # there and shoud be
								print "VERIFY:\tEmail found for "+str(account)+"\tPASS"
								self.results.append("VERIFY:\tEmail found for "+str(account)+"\tPASS\n")
								self.counter += 1
								break
							if status == "Absent":  # there and shouldn't be
								print "VERIFY:\tEmail not found for "+str(account)+"\tFAIL"
								self.results.append("VERIFY:\tEmail not found for "+str(account)+"\tFAIL\n")
								break
						else: pass
					else:
						pass
				else:
					if status == "Present": #isn't there and it should be
						print "VERIFY:\tEmail found for "+str(account)+"\tFAIL\n"
						self.results.append("VERIFY:\tEmail found for "+str(account)+"\tFAIL\n")
					if status == "Absent":  #isn't there and it shouldn't be
						print "VERIFY:\tEmail not found for "+str(account)+"\tPass"
						self.results.append("VERIFY:\tEmail not found for "+str(account)+"\tPass\n")
						self.counter += 1
		else:
			print " no email search was conducted because the inbox is empty"
		return self.counter ,self.results


	def emptyInbox(self):
		"""This function empties the ENTIRE Jostle Mailinator Inbox """
		from selenium import webdriver
		from selenium.common.exceptions import NoSuchElementException

		allMsgs = jostleMailinator.getEmail(self)
		emailID = []
		try:
			for lib in allMsgs:
				emailID.append(lib["id"])
			print "There are "+str(len(emailID))+" emails in the inbox"
			try:
				self.driver = webdriver.Firefox()
				self.driver.implicitly_wait(10)
				self.driver.get("http://mailinatorpro.com/")
				self.driver.find_element_by_link_text("I already have an account").click()
				self.driver.find_element_by_id("login-username-field").send_keys("Ship1Stop2")
				self.driver.find_element_by_id("login-password-field").send_keys("119WestPender")
				self.driver.find_element_by_link_text("Login").click()
				raw_input("You are about to empty the inbox. To proceed hit Enter")
				for j,id in enumerate(emailID):
					self.driver.find_element_by_id(str(id)).click()
					self.driver.find_element_by_link_text("Delete").click()
					time.sleep(1)
					print "Deleting email #"+str(j+1)
				self.driver.close()
			except NoSuchElementException:  pass
		except TypeError:
			print "This inbox is already empty"




if __name__ == "__main__":
	res = {"P":0}
	accounts = ["Leo.Laporte@mailinator.com","Jason.Howell@mailinator.com","Tom.Merritt@mailinator.com","Amber.MacArthur@mailinator.com","Andy.Ihnatko@mailinator.com","Brian.Brushwood@mailinator.com","Catherine.Hall@mailinator.com","Denise.Howell@mailinator.com","Eileen.Rivera@mailinator.com","Gina.Trapani@mailinator.com","Iyaz.Akhtar@mailinator.com","Jeff.Jarvis@mailinator.com","Sarah.Lane@mailinator.com","Scott.Johnson@mailinator.com","Veronica.Belmont@mailinator.com","dick@mailinator.com","norman.wiederick@mailinator.com","jack.ho@mailinator.com","robert.ruttan@mailinator.com","eoin.gaughran@mailinator.com","louise.bernard@mailinator.com","paul.mizgala@mailinator.com","gordon.miller@mailinator.com","tim.adams@mailinator.com","hamad.thegreat.deshmukh@mailinator.com","homeless@mailinator.com","landocalrissian@mailinator.com","princessleia@mailinator.com"]
	for i,entry in enumerate(accounts):
		accounts[i] = entry.replace("@mailinator.com","@Ship1Stop2.mailinatorpro.com")

	subject = "Han Solo has invited you to a new to a new Discussion"
	status = "Present"
	output = ["header"]

	checkemail = jostleMailinator()
	count,out = checkemail.emailsVerify(emails=accounts, status=status, subject=subject, window=100, time=1377641421.992)
	#res["P"]+=count
	#print res["P"]
	#checkemail.emptyInbox()
