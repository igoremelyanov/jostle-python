"""
	making a class for checking mailinator for email notificaions sent by Jostle
"""


class Mailinator:

	def __init__(self, driver, subject, output, counter):
		from selenium.common.exceptions import NoSuchElementException
		""" 'driver' is a webdriver object such as driver = webdriver.Firefox()"""
		from selenium.common.exceptions import NoSuchElementException 
		self.driver = driver
		self.subject = subject
		self.output = output
		self.counter = counter
		print "INFO:\tStarting to look through emails"
		output.append("INFO:\tStarting to look through emails\n")
		
	def lookInside(self, usernames, status):
		self.usernames = usernames
		self.status = status #determines whether you are looking for the email to be there or not
		baseURL = "http://mailinator.com/inbox.jsp?to="
		for name in self.usernames:
			mailURL = baseURL + str(name)
			self.driver.get(mailURL)    #navigate to mailbox with URL
			print "INFO:\tEntering " + name + "@mailinator.com"
			self.output.append("INFO:\tEntering " + name + "@mailinator.com\n")
			try:
				idstring = self.driver.find_element_by_id("InboxNameCtrl")
				print "INFO:\tLocated Inbox Name"
				self.output.append("INFO:\tLocated Inbox Name\n")
				boxname = idstring.text
				if boxname == "Inbox for: " + name:
					print "INFO:\tSuccessfully found " + name + " inbox"
					self.output.append("INFO:\tSuccessfully found " + name + " inbox\n")
					print "Looking for email with Subject: " + self.subject
					self.output.append("INFO:\tLooking for email with Subject: " + self.subject+"\n")
				for i in range(2):
					try:
						if i == 0:
							subjectString = self.driver.find_element_by_xpath("//ul[@id='mailcontainer']/li/a/div[2]")
						else:
							subjectString = self.driver.find_element_by_xpath("//ul[@id='mailcontainer']/li"+str(i+1)+"/a/div[2]")
						if self.subject == subjectString.text:
							if self.status == "Present":
								print "should be there and i found it"
								print "VERIFY:\tJostle Email Present\tPASS"		#should be there and i found it
								self.output.append("VERIFY:\tJostle Email Present\tPASS\n")
								self.counter["P"] += 1
								break
							elif self.status == "Absent":
								print "shouldn't be there and i found it"
								print "VERIFY:\tJostle Email Absent\tFAIL"		#shouldn't be there and i found it
								self.output.append("VERIFY:\tJostle Email Absent\tFAIL\n")
								break
					except NoSuchElementException:
						pass
				else:
					if self.status == "Absent":		
						print "shouldn't be there and couldn't find it"
						print "VERIFY:\tJostle Email Absent\tPASS"				#shouldn't be there and couldn't find it
						self.output.append("VERIFY:\tJostle Email Absent\tPASS\n")
						self.counter["P"] += 1
					else:
						print "should be there and couldn't find it"
						print "VERIFY:\tJostle Email Present\tFAIL"				#should be there and couldn't find it
						self.output.append("VERIFY:\tJostle Email Present\tFAIL\n")
			except NoSuchElementException:
				print "INFO:\tCouldn't find inbox name"
				self.output.append("INFO:\tCouldn't find inbox name\n")
						
		
if __name__ == "__main__":
	from selenium import webdriver
	from selenium.common.exceptions import NoSuchElementException   #exception for missing element
	from selenium.common.exceptions import NoSuchFrameException     #exception for missing iframe
	
	driver = webdriver.Firefox()
	driver.implicitly_wait(20)
	
	logins = ["jasonjones","zaphodbeeblebrox"]
	subject = "testing1234"
	output = []
	counter = {"P":0}
		
	mailinator = Mailinator(driver, subject, output, counter)
	mailinator.lookInside(logins, status = "Present")
	driver.quit()




