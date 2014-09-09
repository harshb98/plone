password = "******"
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.ElementTree as ET
import datetime
import os
import urllib2
##password needs to replace ******
import os
#for xml retreval
from xml.dom import minidom
from datetime import datetime
#for getting the name of the admin
import Zope2
#for creating person within fsd object
from AccessControl.SecurityManagement import newSecurityManager
import sys 
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
import time
import urllib
import re
onlineXML = False
import datetime
curr_year = datetime.datetime.now()
curr_year = curr_year.year  #2014
prev_year = curr_year-1   #2013
next_year = curr_year+1   #2015
school_year = str(curr_year)+"-"+str(next_year) ##2014-2015
class Profiles2:
	fullname = ""
	username = ""
	pci = ""
	education = ""
	rank = ""
	usernameArray = []
	certifications = ""
	presentations = ""
	awards = ""
	service = ""
	grants = ""
	publications = ""
	conferences = ""
	memberships = ""
	expertise = ""
	resume = ""
	
	AC_YEAR = ""
	def populate_admin(self, individual, username,opener):
		#####print "inside admin"
		start = time.time()
		ploneOnServer = False
		container = []
		user = []
		count1 = 0
		catPlusPos = ""
		categoryArray = []
		categoryOnly = []
		catHolder = []
		rank = ""
		index = 0
		active = False
		old_year = True
		#onlineXML is set to False at the top of this page, and will more than likely not be used, but 
		#I am keeping this if statement here in case we decide to use it to speed up the code
		if onlineXML == True:
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/admin.xml')			
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/admin.xml')
			root = tree2.getroot()
		#This else statement uses the "opener" passed in to open the url to the xml file, and the Element Tree package is used to get to the root of the file.
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/ADMIN'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		#notes and RANKS are just declared variables used later on in this method. 
		notes = ""
		RANK = ""
		#nameArray is populate with the usernames of the faculty and staff in order to get the index of the specific faculty/staff to get there correct information
		nameArray = []
		l = 0
		rc = 0 #record count
		#this for loop goes iterates through the recored tags in the admin xml, and populates the nameArray with the the username in the record tag
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			#record.get('username') is how you get the username attribute in the record tag. You can use this to get other attributes as well, just use the attribute name.
			nameArray.append(record.get('username'))
		for person in nameArray:
			start = time.time()
			if individual == True:
				person = username
				if person not in nameArray:
					active = False
					break
			index = nameArray.index(person)
			categoryOnly = []
			categoryArray = []
			for admin in root[index].iter("{http://www.digitalmeasures.com/schema/data}ADMIN"):                 
				count = len(admin.findall("{http://www.digitalmeasures.com/schema/data}ADMIN_DIR"))
				catHolder.append(count)
				catCount = 0
				error = "error"
				rightYearCount = 0
				try:
					RANK = str(admin.find("{http://www.digitalmeasures.com/schema/data}RANK").text).strip()
				except AttributeError:
					RANK = ""
				try:
					AC_YEAR = str(admin.find("{http://www.digitalmeasures.com/schema/data}AC_YEAR").text).strip()
				except AttributeError:
					AC_YEAR = ""
				print "AC_YEAR "+AC_YEAR
				try:
					EMPLOYMENT_STATUS = str(admin.find("{http://www.digitalmeasures.com/schema/data}EMPLOYMENT_STATUS").text).strip()
				except AttributeError:
					EMPLOYMENT_STATUS = ""
				if AC_YEAR == school_year and EMPLOYMENT_STATUS == "Active":
					active = True
#####					print count1
					count1+=1
					for adminDir in admin.iter("{http://www.digitalmeasures.com/schema/data}ADMIN_DIR"): 
					        try:
					            CATEGORY = str(adminDir.find("{http://www.digitalmeasures.com/schema/data}CATEGORY").text).strip()
					        except AttributeError:
					            CATEGORY = ""
					        try:
					            POSITION = str(adminDir.find("{http://www.digitalmeasures.com/schema/data}POSITION").text).strip()
					        except AttributeError:
					            POSITION = "  "
					        catCount=catCount+1
					        if CATEGORY != "":
					            if CATEGORY not in categoryOnly:
					        		categoryOnly.append(CATEGORY)
					            if CATEGORY == "College of Business Dean's Office" and POSITION is not "  ":
					                catPlusPos = POSITION
					                if(CATEGORY not in categoryOnly):
					                    categoryOnly.append(CATEGORY)
					                if(catPlusPos not in categoryArray):
					                    categoryArray.append(catPlusPos)
					            elif POSITION is "  " and CATEGORY is not "":
					                if(CATEGORY not in categoryOnly):
					                    categoryOnly.append(CATEGORY)
					            elif POSITION is not "  " and "None" not in POSITION and CATEGORY is not "":
					                catPlusPos = POSITION+", "+CATEGORY
					                if(CATEGORY not in categoryOnly):
					                    categoryOnly.append(CATEGORY)
					                if(catPlusPos not in categoryArray):
					                    categoryArray.append(catPlusPos)
					if individual != True:
						testMethod(person, opener, RANK,categoryArray, categoryOnly)
						l = 0
						for o in categoryOnly:
							l+=1
						break
				if individual == True:
					break
			if individual == True:
					break
		return categoryArray, RANK, categoryOnly, active

	def generatePCI(self, person, opener, Rank, categories):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/pci.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/pci.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/PCI'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		summary = ""
		notes = ""
		nameArray = []
		l = 0
		rc = 0 # record count
		index = 0
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			for pci in root[index].iter("{http://www.digitalmeasures.com/schema/data}PCI"):
				l = l+1
				ID = person
				fname = str(pci.find("{http://www.digitalmeasures.com/schema/data}FNAME").text)
				lname = str(pci.find("{http://www.digitalmeasures.com/schema/data}LNAME").text)
				try:
					mname = str(pci.find("{http://www.digitalmeasures.com/schema/data}MNAME").text)
				except AttributeError:
					mname = "None "
				try:
					OPHONE = str(pci.find("{http://www.digitalmeasures.com/schema/data}OPHONE").text)
				except AttributeError:
					OPHONE = ""
				try:
					BUILDING = str(pci.find("{http://www.digitalmeasures.com/schema/data}BUILDING").text)
				except AttributeError:
					BUILDING = ""
				try:
					rank = str(pci.find("{http://www.digitalmeasures.com/schema/data}RANK").text)
				except AttributeError:
					rank = ""
				try:
					try:
						notes = str(pci.find("{http://www.digitalmeasures.com/schema/data}NOTES").text)
					except UnicodeEncodeError:
						notes = notes.encode('ascii', 'ignore')
				except AttributeError:
					notes = ""
				if "None" in notes:
					notes = ""
				try:
					resume = str(pci.find("{http://www.digitalmeasures.com/schema/data}UPLOAD_BIO").text)
					resume = "<p>Click here for <a href = https://titanfiles.uwosh.edu/groups/COBDigitalMeasures/"+resume+"> full resume</a></p>"
				except AttributeError:
					resume = ""
				self.resume = resume
				expCount = 0
				otherCount = 0
				MoreEXPERTISE = ""
				temp = ""
				expertiseArray = []
				for exp in pci.iter("{http://www.digitalmeasures.com/schema/data}PCI_EXPERTISE"):
					temp = str(exp.find("{http://www.digitalmeasures.com/schema/data}EXPERTISE").text)
					if "None" in temp:
						temp = ""
					if temp != "None" and temp != "":
						if temp == "Other":
							#try:
							self.expertise +=str(pci.find("{http://www.digitalmeasures.com/schema/data}EXPERTISE_OTHER").text)+", "
							#except
						else:
							self.expertise +=str(exp.find("{http://www.digitalmeasures.com/schema/data}EXPERTISE").text)+", "
					while (expCount < len(exp)):
						expCount= expCount+1
					expCount = 0
				self.expertise = self.expertise.rstrip(", ")
				if mname == "None":
					mname = ""
					name = fname+" "+lname
				else:
					name = fname+" "+mname+" "+lname
				if OPHONE == "None":
					OPHONE = ""
				if BUILDING == "None":
					BUILDING = ""
				adminArray = []
				p = Profiles2()
				rank = Rank
				positions = categories	
				portal = getSite();
				if hasattr(portal, 'portraits'):
					form_folder = getattr(portal, 'portraits')
					pictureName = person+".jpg"
					if hasattr(form_folder,pictureName):
						summary = summary+"<img  align = \"right\" src = http://www.uwosh.edu/cob/portraits/"+pictureName+"/image_thumb><br>"
						self.pci +="<img  align = \"right\" src = http://www.uwosh.edu/cob/portraits/"+pictureName+"/image_mini><br>"
			        else:
						summary +="<img  align = \"right\" src = http://www.uwosh.edu/cob/portraits/default.jpg/image_thumb><br>"
						output +="<img  align = \"right\" src = http://www.uwosh.edu/cob/portraits/default.jpg/image_mini><br>"
				if rank == '' or rank == "Staff" or rank == "Academic Staff":
					error = "no rank"
				else:
					self.pci +=rank+"\n<br>"
					summary +=rank+"\n<br>"
				t = 0
				for i in positions:
					self.pci +=str(positions[t])+"<br>"
					t = t+1
				self.pci += "<table class = \"inner\">\n<tr>\n<td class =\"office-label\">\nOffice:</td>\n<td class =\"building\">\n"+BUILDING+"\n</td>\n</tr>\n"##
				summary += "<table class = \"inner\">\n<tr>\n<td class =\"office-label\">\nOffice:</td>\n<td class =\"building\">\n"+BUILDING+"\n</td>\n</tr>\n" ##
				self.pci += "<tr>\n<td class =\"phone-label\">\nOffice Phone: </td>\n<td class =\"phone\">\n"+OPHONE+"\n</td>\n</tr>\n" ##
				summary += "<tr>\n<td class =\"phone-label\">\nOffice Phone:</td>\n<td class =\"phone\">\n"+OPHONE+"\n</td>\n</tr>\n"   ##
				self.pci += "<tr>\n<td class =\"email-label\">\nEmail:\n</td>\n<td class =\"email\">\n<a href=mailto:"+ID+"@uwosh.edu>"+ID+"@uwosh.edu</a>\n</td>\n</tr>\n" ##
				summary +="<tr>\n<td class =\"email-label\">\nEmail:\n</td>\n<td class =\"email\">\n<a href=mailto:"+ID+"@uwosh.edu>"+ID+"@uwosh.edu</a>\n</td>\n</tr>\n"   ##
				if len(temp)>0:
					self.pci += "<tr>\n<td class =\"expertise-label\">\nExpertise: </td><td class =\"expertise\">\n"+self.expertise+"</td>\n</tr>\n</table>\n"
					summary += "<tr>\n<td class =\"expertise-label\">\nExpertise: </td><td class =\"expertise\">\n"+self.expertise+"</td>\n</tr>\n</table>\n"
				self.pci +="<br>"+notes
				self.fullname = name
				self.username = ID
				self.usernameArray.append(self.username)
				self.rank = rank
				if "None" in self.pci:
					self.pci = self.pci.replace("None", "")
				if "None" in summary:
					summary = self.pci.replace("None", "")
				break
		return self.pci, summary

	def generateEducation(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/education.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/education.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/EDUCATION'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		nameArray = []
		l = 0
		rc = 0 # record count
		index = 0
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			i = index
			education = ""
			for edu in root.iter("{http://www.digitalmeasures.com/schema/data}EDUCATION"):
				k = 1
				try:
					for edu in root[i][k].iter("{http://www.digitalmeasures.com/schema/data}EDUCATION"):
						try:
							highestDeg = str(edu.find("{http://www.digitalmeasures.com/schema/data}HIGHEST").text)
						except AttributeError:
							highestDeg = ""
						if highestDeg == "Yes":
							deg = str(edu.find("{http://www.digitalmeasures.com/schema/data}DEG").text)+""
							major = str(edu.find("{http://www.digitalmeasures.com/schema/data}MAJOR").text)+". "
							SUPPAREA = str(edu.find("{http://www.digitalmeasures.com/schema/data}SUPPAREA").text)+","
							school = str(edu.find("{http://www.digitalmeasures.com/schema/data}SCHOOL").text)+", "
							YR_COMP = str(edu.find("{http://www.digitalmeasures.com/schema/data}YR_COMP").text)
							if major == "none.":
								major = ""
							if deg == "none":
								deg = ""
							if SUPPAREA == "None,":
								SUPPAREA = ""
							if school == "None,":
								school = ""
							if YR_COMP == "None,":
								YR_COMP = ""
							self.education = deg+" "+major+" "+SUPPAREA+" "+school+YR_COMP
							k = k+1
							break
						else:
							k = k+1
					break
				except IndexError:
					education = "no education"
		if "None" in self.education:
			self.education = self.education.replace("None", "")
		return self.education

	def generateAwards(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/awards.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/awards.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/AWARDHONOR'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		nominated = ""
		text = ""
		nameArray = []
		index = 0
		awards = ""
		i = 0
		itemCount = 0
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			i = index
			for award in root[index].iter("{http://www.digitalmeasures.com/schema/data}AWARDHONOR"):
				try:
					PUB_INTERNET = str(award.find("{http://www.digitalmeasures.com/schema/data}PUB_INTERNET").text)
				except AttributeError:
					PUB_INTERNET = "No"
				if PUB_INTERNET == "Yes":
					awardName = str(award.find("{http://www.digitalmeasures.com/schema/data}NAME").text)+", "
					if  "Other" in awardName:
						try:
							awardName = str(award.find("{http://www.digitalmeasures.com/schema/data}NAME_OTHER").text)+", "
						except UnicodeEncodeError:
							awardName = awardName.encode('ascii', 'ignore')
					try:
						nominated = str(award.find("{http://www.digitalmeasures.com/schema/data}NOMREC").text)+", "
					except AttributeError:
						nominated = "None,"
					try:
						org = str(award.find("{http://www.digitalmeasures.com/schema/data}ORG").text)+", "
					except AttributeError:
						org = "None,"
					try:
						month = str(award.find("{http://www.digitalmeasures.com/schema/data}DTM_DATE").text)+""
					except AttributeError:
						month = "None"
					try:
						day = str(award.find("{http://www.digitalmeasures.com/schema/data}DTD_DATE").text)+","
					except AttributeError:
						day = "None,"
					try:
						year = str(award.find("{http://www.digitalmeasures.com/schema/data}DTY_DATE").text)+","
					except AttributeError:
						year = "None,"
					if month is not "None" and year is not "None,":
						if day == "None,":
							#day = ""
							date1 = str(month)+" "+str(year)
						if month == "None":
							date1 = str(year)
						else:
							date1 = str(month)+" "+str(day)+" "+str(year)
					if awardName is "None," or org is "None,":
						condition = False
					else:
						itemCount+=1
						try:
							awardCombined = str(awardName)+str(nominated)+str(org)+date1
						except UnicodeEncodeError:
							awardCombined = awardCombined.encode('ascii', 'ignore')
						awardCombined
						awards = str(awards)+"<li>\n"+str(fixPuncuation(awardCombined))+"\n</li>\n"
		if  itemCount > 1:
			awards ="\n<h2>Awards</h2>\n<ul>"+awards
			awards+="</ul>\n"
		elif itemCount == 1:
			awards ="\n<h2>Award</h2>\n<ul>"+awards
			awards+="</ul>\n"
		self.awards = awards
		if "None" in self.awards:
			self.awards = self.awards.replace("None", "")
		return self.awards

	def generateCertifications(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/cert.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/cert.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/LICCERT'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		finalString = ""
		text = ""
		nameArray = []
		index = 0
		member = ""
		itemCount = 0
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			END_END =""
			for cert in root[index].iter("{http://www.digitalmeasures.com/schema/data}LICCERT"):
 				END_END = str(cert.find("{http://www.digitalmeasures.com/schema/data}END_END").text)+","
  				if END_END == "None,":
					try:
						TITLE = str(cert.find("{http://www.digitalmeasures.com/schema/data}TITLE").text)+","
					except AttributeError:
						TITLE = ""
					try:
						COPY = str(cert.find("{http://www.digitalmeasures.com/schema/data}COPY").text)+","
					except AttributeError:
						COPY = ""
					try:
						START_START = str(cert.find("{http://www.digitalmeasures.com/schema/data}START_START").text)
					except AttributeError:
						START_START = ""
					try:
						DTM_START = " "+str(cert.find("{http://www.digitalmeasures.com/schema/data}DTM_START").text)+", "
					except AttributeError:
						DTM_START = ""
					if "None" in DTM_START:
						DTM_START = ""
					try:
						DTY_START = str(cert.find("{http://www.digitalmeasures.com/schema/data}DTY_START").text)
					except AttributeError:
						DTY_START = ""
					if "None" in DTY_START:
						DTY_START = ""
					if "None" in TITLE:
						condition = False
						member = ""
					else:
						itemCount+=1
						member = TITLE+DTM_START+DTY_START
						member = fixPuncuation(member)
						member ="<li>\n"+member+"\n</li>\n" 
						finalString+=member         
	        if itemCount > 0:
	            finalString = "<h2>Certifications</h2>\n<ul>"+finalString
	        else:
	        	finalString = "<h2>Certification</h2>\n<ul>"+finalString
		finalString +="</ul>\n"
		if itemCount <1:
			finalString = ""
		self.Certification = finalString
		if "None" in self.Certification:
			self.Certification = self.Certification.replace("None", "")
		return self.Certification

	def generateGrants(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/grants.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/grants.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/CONGRANT'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		finalString = "<ul>\n"
		text = ""
		nameArray = []
		index = 0
		grants = ""
		itemCount = 0
		published = 0
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			pub_internet = ""
			for grants in root[index].iter("{http://www.digitalmeasures.com/schema/data}CONGRANT"):
				try:
					pub_internet = str(grants.find("{http://www.digitalmeasures.com/schema/data}PUB_INTERNET").text)
				except AttributeError:
					pub_internet = "no"
				if pub_internet == "Yes":
					published = published+1
					TYPE = str(grants.find("{http://www.digitalmeasures.com/schema/data}TYPE").text)+". "
					if "None" in TYPE:
						TYPE = ""
					TITLE = ' "'+str(grants.find("{http://www.digitalmeasures.com/schema/data}TITLE").text).rstrip()+'"'
					if "None" in TITLE:
						TITLE = ""
					CO_INVESTIGATORS = "Co-investigator(s): "+str(grants.find("{http://www.digitalmeasures.com/schema/data}CO_INVESTIGATORS").text)+". "
					if "None" in CO_INVESTIGATORS:
						CO_INVESTIGATORS = ""
					SPONORG = " Awarded by "+str(grants.find("{http://www.digitalmeasures.com/schema/data}SPONORG").text)+". "
					if "None" in SPONORG:
						SPONORG = ""
					TERM_START = " "+str(grants.find("{http://www.digitalmeasures.com/schema/data}TERM_START").text)+","
					if "None" in TERM_START:
						TERM_START = ""
					CLASSIFICATION = " "+str(grants.find("{http://www.digitalmeasures.com/schema/data}CLASSIFICATION").text)+". "
					if "None" in CLASSIFICATION :
						CLASSIFICATION = ""
					TYY_TERM = "("+str(grants.find("{http://www.digitalmeasures.com/schema/data}TYY_TERM").text)+")."
					if "None" in TYY_TERM:
						TYY_TERM = ""                
					grants = TYPE+TYY_TERM+TITLE+SPONORG+CLASSIFICATION+CO_INVESTIGATORS
					grants = fixPuncuation(grants)
					grants ="<li>\n"+grants+"\n</li>\n"
					finalString+=grants
	        finalString+="</ul>\n"
	        if published > 0:
	            finalString = "<h2>Grants</h2>\n"+finalString
	        elif published == 0:
	        	finalString = "<h2>Grants</h2>\n"+finalString
	        try:
	            finalString=finalString
	        except UnicodeEncodeError:
	            text = finalString.encode('ascii', 'ignore')
	            finalString+="\n"
	    	if published <1:
	        	finalString = ""
	        self.grants = finalString
	        if "None" in self.grants:
				self.grants = self.grants.replace("None", "")
	    	return self.grants

	def generateService(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/service.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/service.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/GENSERVE'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		finalString = ""
		text = ""
		nameArray = []
		index = 0
		string = ""
		itemCount = 0
		published = -1
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			pub_internet = ""
			for service in root[index].iter("{http://www.digitalmeasures.com/schema/data}GENSERVE"):
				try:
					pub_internet = str(service.find("{http://www.digitalmeasures.com/schema/data}INTERNET").text)
				except AttributeError:
					pub_internet ="None"
				if pub_internet != "None" and pub_internet != "No":
					published = published+1
					TYPE = str(service.find("{http://www.digitalmeasures.com/schema/data}TYPE").text)+": "
					if "None" in TYPE:
						TYPE = ""
					ORG = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}ORG").text)+","
					if "None" in ORG:
						ORG = ""
					ROLE = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}ROLE").text)+", "
					if "None" in ROLE:
						ROLE = ""
					if "other" in ROLE:
						ROLEOTHER = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}ROLEOTHER").text)+","
						if "None" in ROLEOTHER:
							ROLEOTHER = ""
						ROLE = ROLEOTHER
					RESPONSIBILITIES = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}RESPONSIBILITIES").text)+","
					if "None" in RESPONSIBILITIES:
						RESPONSIBILITIES = ""
					DTM_START = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}DTM_START").text)+" "
					if "None" in DTM_START:
						DTM_START = ""
					DTY_START = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}DTY_START").text)+"-"
					if "None" in DTY_START:
						DTY_START = ""
					DTY_END = " "+str(service.find("{http://www.digitalmeasures.com/schema/data}DTY_END").text)+","
					if "None" in DTY_END:
						DTY_END = "Present"
					string = TYPE+ORG+ROLE+DTM_START+DTY_START+DTY_END
					s = finalString[len(finalString)-1:]
					if s == ',':
						finalString = finalString.rstrip(',')
						finalString += "<li>"+string+"</li>"
					else:
						finalString += "<li>"+string+"</li>"
        	if published> 0:
				finalString ="<h2>Service</h2>\n"+"<ul>\n"+finalString
				finalString += "</ul>\n"
        	elif published == 0:  
				finalString ="<h2>Service</h2>\n"+"<ul>\n"+finalString
				finalString += "</ul>\n"      	
		self.service = finalString
		if "None" in self.service:
			self.service = self.service.replace("None", "")
		return self.service

	def generateProfessionalMembership(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/pm.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/pm.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/MEMBER'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		membership = ""
		text = ""
		nameArray = []
		index = 0
		Profmember = ""
		itemCount = 0
		published = 0
		condition = True
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			for mem in root[index].iter("{http://www.digitalmeasures.com/schema/data}MEMBER"):
				Profmember = ""
				try:
					pub_internet = str(mem.find("{http://www.digitalmeasures.com/schema/data}INTERNET").text)
				except AttributeError:
					pub_internet ="None"
				if pub_internet != "None" and pub_internet != "No":
					published = published+1
					try:
						TITLE = " "+str(mem.find("{http://www.digitalmeasures.com/schema/data}TITLE").text)+"."
					except AttributeError:
						TITLE = "None"
					if "None" not in TITLE:
						published+=1
						Profmember = TITLE
						if len(Profmember)>0:
							Profmember = fixPuncuation(Profmember)
							Profmember ="<li>"+Profmember+"</li>" 
							membership=membership+Profmember
					else:
						condition = False
						break
			
			if published > 0:
				membership = "<h2>Professional Memberships</h2>"+membership
				membership = membership+"</ul>"
			elif published == 0:
				membership = "<h2>Professional Membership</h2>"+membership
				membership = membership+"</ul>"
			try:
				membership+="\n"
			except UnicodeEncodeError:
				text = membership.encode('ascii', 'ignore')
				membership+=text
			if published <1:
				membership = ""
		self.membership = membership
		if "None" in self.membership:
			self.membership = self.membership.replace("None", "")
		return self.membership

	def generateConference(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/conf.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/conf.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/PRESENT_CONFERENCE'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		text = ""
		nameArray = []
		index = 0
		conferenceString = ""
		authors = ""
		itemCount = 0
		published = 0
		condition = True
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			pub_internet = ""
			for conference in root[index].iter("{http://www.digitalmeasures.com/schema/data}PRESENT_CONFERENCE"):
				try:
					pub_internet = str(conference.find("{http://www.digitalmeasures.com/schema/data}PUB_INTERNET").text)
				except AttributeError:
					pub_internet ="None"
				if pub_internet != "None" and pub_internet != "No":
					published+=1
					try:
						NAME = ""
						try:
							NAME = ' Paper presented at '+str(conference.find("{http://www.digitalmeasures.com/schema/data}NAME").text)+", "
						except UnicodeEncodeError:
							NAME = NAME.encode('ascii', 'ignore')
					except AttributeError:
						NAME ="None"
					try:
						ORG = ' "'+str(conference.find("{http://www.digitalmeasures.com/schema/data}ORG").text)+'"'
					except AttributeError:
						ORG ="None"
					if "None" in ORG:
						ORG = ""
					try:
						LOCATION = ' '+str(conference.find("{http://www.digitalmeasures.com/schema/data}LOCATION").text)+"."
					except AttributeError:
						LOCATION ="None"
					try:
						DESC = ' '+str(conference.find("{http://www.digitalmeasures.com/schema/data}DESC").text)+","
					except AttributeError:
						DESC ="None"
					try:
						DTM_PRESENT = ' '+str(conference.find("{http://www.digitalmeasures.com/schema/data}DTM_PRESENT").text)+" "
					except AttributeError:
						DTM_PRESENT ="None"
					try:
						DTY_PRESENT = ' '+str(conference.find("{http://www.digitalmeasures.com/schema/data}DTY_PRESENT").text)+"."
					except AttributeError:
						DTY_PRESENT ="None"
					try:
						TITLE = ' '+str(conference.find("{http://www.digitalmeasures.com/schema/data}TITLE").text)+"."
					except AttributeError:
						TITLE ="None"
					FNAME = ""
					MNAME = ""
					LNAME = ""
					users = []
					authorArr = []
					authorCount = 0
					for aut in conference.iter("{http://www.digitalmeasures.com/schema/data}PRESENT_CONFERENCE_AUTH"):
						count = len(conference.findall("{http://www.digitalmeasures.com/schema/data}PRESENT_CONFERENCE_AUTH"))
						try:
							FNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}FNAME").text)[:1]+"."
						except AttributeError:
							FNAME = ""
						try:
							MNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}MNAME").text)+". "
						except AttributeError:
							MNAME = ""
						try:
							LNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}LNAME").text)+", "
						except AttributeError:
							LNAME = ""
						if "None" in FNAME:
							FNAME = ""
						if "None" in MNAME :
							MNAME = ""
						else:
							MNAME = MNAME[:1]+"."
						if "None" in LNAME:
							LNAME = ""
						authorCount+=1
						if (authorCount-1 == 0):
							authors = authors+" "+LNAME+FNAME+MNAME
						elif (authorCount == 1):
							authors = authors+" & "+LNAME+FNAME+MNAME
						elif (authorCount > 1):
							if (authorCount+1 > count):
								authors = authors+", & "+LNAME+FNAME+MNAME
							else:
								authors = authors+", "+LNAME+FNAME+MNAME
					temp = authors+" "+TITLE+NAME+ ORG+ LOCATION\
					+DESC+DTM_PRESENT+DTY_PRESENT
					temp = fixPuncuation(temp)
					temp ="<li>"+temp+"</li>" 
					conferenceString=conferenceString+temp
					if "None" in conferenceString:
						conferenceString = conferenceString.replace("None", "")
					temp = ""
				authors = ""
			conferenceString+="\n</ul>"
		if published >1:
			conferenceString = "<h2>Conferences</h2>"+"<ul>\n"+conferenceString 
			try:
 				conferenceString+="\n"
			except UnicodeEncodeError:
				text = conferenceString.encode('ascii', 'ignore')
		elif published == 1:
			conferenceString = "<h2>Conference</h2>"+"<ul>\n"+conferenceString 
			try:
 				conferenceString+="\n"
			except UnicodeEncodeError:
				text = conferenceString.encode('ascii', 'ignore')
		self.conferences = conferenceString
		if "None" in self.conferences:
			self.conferences = self.conferences.replace("None", "")
		return self.conferences

	def generateProf(self, person, opener):
		if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/prof.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/prof.xml')
			root = tree2.getroot()
		else:
			url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/PRESENT_PROFESSIONAL'
			opener.open(url)
			urllib2.install_opener(opener)
			req = urllib2.Request(url)
			response = urllib2.urlopen(req)
			info = response.read()
			root = ET.fromstring(info)
		text = ""
		nameArray = []
		index = 0
		presentationString = ""
		profPres = ""
		authors = ""
		itemCount = 0
		published = 0
		condition = True
		for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
		if person in nameArray:
			index = nameArray.index(person)
			pub_internet = ""
			for presentations in root[index].iter("{http://www.digitalmeasures.com/schema/data}PRESENT_PROFESSIONAL"):
				try:
					pub_internet = str(presentations.find("{http://www.digitalmeasures.com/schema/data}PUB_INTERNET").text)
				except AttributeError:
					pub_internet ="None"
				if pub_internet != "None" and pub_internet != "No":
					published+=1
					try:
						TYPE = str(presentations.find("{http://www.digitalmeasures.com/schema/data}TYPE").text)+": "
					except AttributeError:
						TYPE = ""
					try:
						TYPEOTHER = str(presentations.find("{http://www.digitalmeasures.com/schema/data}TYPEOTHER").text)+": "
					except AttributeError:
						TYPEOTHER = ""
					try:
						TITLE = str(presentations.find("{http://www.digitalmeasures.com/schema/data}TITLE").text)+". "
					except AttributeError:
						TITLE = ""
					try:
						DTY_DATE = str(presentations.find("{http://www.digitalmeasures.com/schema/data}DTY_DATE").text)+". "
					except AttributeError:
						DTY_DATE = ""
					try:
						ORG = "Presented to "+str(presentations.find("{http://www.digitalmeasures.com/schema/data}ORG").text)+","
					except AttributeError:
						ORG = ""
					if ( "Other" in TYPE):
						TYPEOTHER = TYPEOTHER
					else:
						TYPEOTHER = TYPE
					FNAME = ""
					MNAME = ""
					LNAME = ""
					users = []
					authorArr = []
					authorCount = 0
					for aut in presentations.iter("{http://www.digitalmeasures.com/schema/data}PRESENT_PROFESSIONAL_AUTH"):
						count = len(presentations.findall("{http://www.digitalmeasures.com/schema/data}PRESENT_PROFESSIONAL_AUTH"))
						try:
							FNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}FNAME").text)[:1]+"."
						except AttributeError:
							FNAME = "None"
						try:
							MNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}MNAME").text)+". "
						except AttributeError:
							MNAME = "None"
						try:
							LNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}LNAME").text)+", "
						except AttributeError:
							LNAME = "None"
						if "None" in FNAME:
							FNAME = ""
						if "None" in MNAME:
							MNAME = ""
						else:
							MNAME = MNAME[:1]+"."
						if "None" in LNAME:
							LNAME = ""
						authorCount+=1
						if (authorCount-1 == 0):
							authors = authors+LNAME+FNAME+MNAME
						elif (authorCount == 1):
							authors = authors+" & "+LNAME+FNAME+MNAME
							authors = authors[1:]
						elif (authorCount > 1):
							if (authorCount+1 > count):
								authors = authors+", & "+LNAME+FNAME+MNAME
							else:
								authors = authors+", "+LNAME+FNAME+MNAME
					profPres = authors+" "+ DTY_DATE+TYPEOTHER+ TITLE+ORG
					authors = ""
					profPres = fixPuncuation(profPres)
					profPres ="<li>"+profPres+"</li>" 
					presentationString=presentationString+profPres
			presentationString = presentationString
	        if published > 0:
	            presentationString = "<h2>Professional Presentations</h2>"+"<ul>"+presentationString
	            presentationString = presentationString+"</ul>"	 
	        elif published == 0:
	            presentationString = "<h2>Professional Presentation</h2>"+"<ul>"+presentationString
	            presentationString = presentationString+"</ul>"	 
	        try:
	            presentationString+="\n"
	        except UnicodeEncodeError:
	            text = presentationString.encode('ascii', 'ignore')
	        presentationString+=text
	        if published <1:
		        presentationString = ""
	        if "None" in self.presentations:
				self.presentations = self.presentations.replace("None", "")
        	return self.presentations

	def generatePub(self, person, opener):
	    if onlineXML == True:
			tree = ET.parse('/Users/cobstu01/Desktop/xmlFiles/pub.xml')
			tree2 = ET.parse('http://webdev.cs.uwosh.edu/students/harshb98/xmlFiles/pub.xml')
			root = tree2.getroot()
	    else:
		    url = 'https://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business/INTELLCONT'
		    opener.open(url)
		    urllib2.install_opener(opener)
		    req = urllib2.Request(url)
		    response = urllib2.urlopen(req)
		    info = response.read()
		    root = ET.fromstring(info)
	    import time
	    j = 0
	    pub = []
	    linkString = ""
	    count = 0
	    condition = True
	    nodeCount = 0
	    index = 0
	    forthcoming = []
	    forthcomingContainer = []
	    finished = False
	    user = []
	    users2 = []
	    linkContainer = []
	    linkCount = 0
	    hasLink = False
	    JournalArticle = []
	    BookChapter = []
	    Book = []
	    ArticleContainingCitation = []
	    ConferenceProceeding = []
	    BookReview = []
	    BroadcastMedia = []
	    Cases = []
	    Chapters = []
	    CitedResearch = []
	    Editorship = []
	    InHousePaper = []
	    InstructionalTextbook = []
	    InstructorsManual = []
	    MagazineTradePublication = []
	    Monographs = []
	    Newsletter = []
	    Newspaper = []
	    regularcolumn = []
	    ResearchReport = []
	    Software = []
	    StudyGuide = []
	    TechnicalReport = []
	    WorkingPaper = []
	    ForthcomingArray = []
	    publishedArray = []
	    authorArray = []
	    identifier = []
	    nameArray = []
	    authors = ""
	    publicationString = ""
	    published = 0
	    i = 0
	    hasPublication = False
	    stringList = ""
	    ploneOnServer = False
	    totalTimeStart = time.time()
	    for record in root.iter("{http://www.digitalmeasures.com/schema/data}Record"):
			nameArray.append(record.get('username'))
	    if person in nameArray:
			index = nameArray.index(person)
			pub_internet = ""
			for publication in root[index].iter("{http://www.digitalmeasures.com/schema/data}INTELLCONT"):
				try:
					pub_internet = str(publication.find("{http://www.digitalmeasures.com/schema/data}PUB_INTERNET").text)
				except AttributeError:
					pub_internet ="None"
				if pub_internet == "Yes":
					published+=1
					try:
						FNAME = str(publication.find("{http://www.digitalmeasures.com/schema/data}FNAME").text)
					except AttributeError:
						FNAME = ""
					try:
						CONTYPE = "("+str(publication.find("{http://www.digitalmeasures.com/schema/data}CONTYPE").text)+")"
					except AttributeError:
						CONTYPE = ""
					if "None" in CONTYPE:
						CONTYPE = " "
					try:
						STATUS = "("+str(publication.find("{http://www.digitalmeasures.com/schema/data}STATUS").text)+"). "
					except AttributeError:
						STATUS = ""
					if "None" in STATUS:
						STATUS = " "
					try:
						DTY_PUB = " ("+str(publication.find("{http://www.digitalmeasures.com/schema/data}DTY_PUB").text)+"). "
					except AttributeError:
						DTY_PUB = ""
					if "None" in DTY_PUB:
						DTY_PUB = " "
					TITLE = ""
					try:
						TITLE = "<span>"+str(publication.find("{http://www.digitalmeasures.com/schema/data}TITLE").text)
						if '"' in TITLE:
							TITLE = TITLE.replace('"',"")
						if TITLE[len(TITLE)-1:].isalpha() == False and TITLE[len(TITLE)-1:].isdigit() == False:
							TITLE = TITLE.strip(TITLE[len(TITLE)-1:])
						TITLE+="</span>. "
					except AttributeError:
						TITLE = ""
					except UnicodeEncodeError:
						TITLE = TITLE.encode('ascii', 'ignore')
					try:
						PUBLISHER = str(publication.find("{http://www.digitalmeasures.com/schema/data}PUBLISHER").text).strip()
					except AttributeError:
						PUBLISHER = ""
					try:
						VOLUME = str(publication.find("{http://www.digitalmeasures.com/schema/data}VOLUME").text)+", "
					except AttributeError:
						VOLUME = ""
					try:
						PAGENUM = "("+str(publication.find("{http://www.digitalmeasures.com/schema/data}PAGENUM").text)+")."
					except AttributeError:
						PAGENUM = ""
					try:
						EDITORS = "in "+str(publication.find("{http://www.digitalmeasures.com/schema/data}EDITORS").text)+" (Eds.), "
					except AttributeError:
						EDITORS = ""
					if "None" in EDITORS:
						EDITORS = ". "
					try:
						TITLE_SECONDARY = str(publication.find("{http://www.digitalmeasures.com/schema/data}TITLE_SECONDARY").text)+". "
					except AttributeError:
						TITLE_SECONDARY = ""
					try:
						PUBCTYST = " "+str(publication.find("{http://www.digitalmeasures.com/schema/data}PUBCTYST").text)+": "
					except AttributeError:
						PUBCTYST = ""
					if "None" in PUBCTYST:
						PUBCTYST = " " 
					FNAME = ""
					MNAME = ""
					LNAME = ""
					users = []
					authorArray = []
					authorCount = 0
					try:
						for aut in publication.iter("{http://www.digitalmeasures.com/schema/data}INTELLCONT_AUTH"):
							count = len(publication.findall("{http://www.digitalmeasures.com/schema/data}INTELLCONT_AUTH"))
							try:
								try:
									FNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}FNAME").text)[:1]+"."
								except UnicodeEncodeError:
									FNAME = publicationString.encode('ascii', 'ignore')
							except AttributeError:
								FNAME = "None"
							try:
								MNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}MNAME").text)+". "
							except AttributeError:
								MNAME = "None"
							try:
								LNAME = str(aut.find("{http://www.digitalmeasures.com/schema/data}LNAME").text)+", "
							except AttributeError:
								LNAME = "None"
							if "None" in FNAME:
								FNAME = ""
							if "None" in MNAME:
								MNAME = ""
							else:
								MNAME = MNAME[:1]+"."
							if "None" in LNAME:
								LNAME = ""
							authorCount+=1
							if (authorCount-1 == 0):
								authors = authors+LNAME+FNAME+MNAME
							elif (authorCount == 1):
								authors = authors+" & "+LNAME+FNAME+MNAME
								authors = authors[1:]
							elif (authorCount > 1):
								if (authorCount+1 > count):
									authors = authors+", & "+LNAME+FNAME+MNAME
								else:
									authors = authors+", "+LNAME+FNAME+MNAME
					except IndexError:
					    error = "error"
					nodeCount = nodeCount+1
					journalArticleCount = 0
					authorArray.append(authors)
					if( "'" in CONTYPE):
					    CONTYPE = CONTYPE.replace(" ", "'")
					if("/" in CONTYPE):
					    CONTYPE = CONTYPE.replace(" ", "/")
					if(CONTYPE == "(Journal Article)"):
					    if (PUBLISHER != ""):
					        PUBLISHER = "<span class=\"italics\">"+PUBLISHER+".</span> "
					    if (STATUS == "(Forthcoming). "):
					        linkString = authors+" "+STATUS+" "+TITLE+PUBLISHER####+VOLUME+PAGENUM
					        linkString = fixPuncuation(linkString)
					        ForthcomingArray.append("<li>"+linkString+"</li>")
					    elif (STATUS == "(Work-in-progress). "):
					        linkString = authors+" "+STATUS+" "+TITLE+PUBLISHER####+VOLUME+PAGENUM
					        linkString = fixPuncuation(linkString)
					        ForthcomingArray.append("<li>"+linkString+"</li>")
					    elif (STATUS == "(Published). "):                       
					        linkString = authors+DTY_PUB+TITLE+PUBLISHER####+VOLUME+PAGENUM
					        linkString = fixPuncuation(linkString)
					        publishedArray.append("<li>"+linkString+"</li>")
					        hasPublication = True
					elif(CONTYPE == "(Book Chapter)"):
						linkString = authors+DTY_PUB+TITLE+EDITORS+TITLE_SECONDARY+PUBCTYST+PUBLISHER.strip()
						linkString = fixPuncuation(linkString)
						BookChapter.append("<li>"+linkString+"</li>")
						hasPublication = True
					elif(CONTYPE == "(Book)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Book.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Article Containing Citation)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    ArticleContainingCitation.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Conference Proceeding)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    ConferenceProceeding.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Book Review)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    BookReview.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Broadcast Media)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Broadcast.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Cases)"):
					    linkString = Fauthors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Cases.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Chapter(s))"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Chapters.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Cited Research)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    CitedResearch.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Editorship)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Editorship.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(In-House Paper)"):
					    temp = contype
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER+temp.strip()
					    linkString = fixPuncuation(linkString)
					    InHousePaper.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Instructional Textbook)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    InstructionalTextbook.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Instructor s Manual)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    JournalArticle.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Magazine Trade Publication"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    MagazineTradePublication.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Monographs)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Monographs.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Newsletter)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Newsletter.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Newspaper)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Newspaper.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Regular Column in Journal or Newspaper)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    regularcolumn.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Research Report"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    ResearchReport.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Software)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    Software.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Study Guide)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    StudyGuide.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Technical Report)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    TechnicalReport.append("<li>"+linkString+"</li>")
					    hasPublication = True
					elif(CONTYPE == "(Working Paper)"):
					    linkString = authors+DTY_PUB+TITLE+PUBLISHER.strip()
					    linkString = fixPuncuation(linkString)
					    WorkingPaper.append("<li>"+linkString+"</li>")
					    hasPublication = True
			        i = i+1
			        authors = ""
			linkLength = 0
			if (hasPublication == True):
				if (len(publishedArray)+len(ForthcomingArray)>0):
				    if (len(publishedArray)+len(ForthcomingArray)>1):
				        stringList +="<h2>Journal Articles</h2><ul>"
				    else:
				        stringList +="<h2>Journal Article</h2><ul>"
				    while (len(ForthcomingArray)>linkLength):
				        stringList+= ForthcomingArray[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1  
				    linkLength = 0
				    while (len(publishedArray)>linkLength):
				        stringList+= publishedArray[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1  
				    stringList+="</ul>"    
				linkLength = 0
				if (len(BookReview)>0):
				    if (len(BookReview)>1):
				        stringList +="<h2>Book Reviews</h2><ul>"
				    else:
				        stringList +="<h2>Book Review</h2><ul>"
				    while (len(BookReview)>linkLength):
				        stringList+=BookReview[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Book)>0):
				    if (len(Book)>1):
				        stringList +="<h2>Books</h2><ul>"
				    else:
				        stringList +="<h2>Book</h2><ul>"
				    while (len(Book)>linkLength):
				        stringList+=Book[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(BookChapter)>0):
				    if (len(BookChapter)>1):
				        stringList +="<h2>Book Chapters</h2><ul>"
				    else:
				        stringList +="<h2>Book Chapter</h2><ul>"
				    while (len(BookChapter)>linkLength):
				        stringList+=BookChapter[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(BroadcastMedia)>0):
				    if (len(BroadcastMedia)>1):
				        stringList +="<h2>Broadcast Medias</h2><ul>"
				    else:
				        stringList +="<h2>Broadcast Media</h2><ul>"
				    while (len(BroadcastMedia)>linkLength):
				        stringList+=BroadcastMedia[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Cases)>0):
				    if (len(Cases)>1):
				        stringList +="<h2>Cases</h2><ul>"
				    else:
				        stringList +="<h2>Case</h2><ul>"
				    while (len(Cases)>linkLength):
				        stringList+=Cases[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Chapters)>0):
				    if (len(Chapters)>1):
				        stringList +="<h2>Chapters</h2><ul>"
				    else:
				        stringList +="<h2>Chapters</h2><ul>"
				    while (len(Chapters)>linkLength):
				        stringList+=Chapters[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(CitedResearch)>0):
				    if (len(CitedResearch)>1):
				        stringList +="<h2>Cited Researchs</h2><ul>"
				    else:
				        stringList +="<h2>Cited Research</h2><ul>"
				    while (len(CitedResearch)>linkLength):
				        stringList+=CitedResearch[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(ConferenceProceeding)>0):
				    if (len(ConferenceProceeding)>1):
				        stringList +="<h2>Conference Proceedings</h2><ul>"
				    else:
				        stringList +="<h2>Conference Proceedings</h2><ul>"
				    while (len(ConferenceProceeding)>linkLength):
				        stringList+=ConferenceProceeding[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Editorship)>0):
				    if (len(Editorship)>1):
				        stringList +="<h2>Editorships</h2><ul>"
				    else:
				        stringList +="<h2>Editorship</h2><ul>"
				    while (len(Editorship)>linkLength):
				        stringList+=Editorship[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(InHousePaper)>0):
				    if (len(InHousePaper)>1):
				        stringList +="<h2>In-House Papers</h2><ul>"
				    else:
				        stringList +="<h2>In-House Paper</h2><ul>"
				    while (len(InHousePaper)>linkLength):
				        stringList+=InHousePaper[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(InstructionalTextbook)>0):
				    if (len(InstructionalTextbook)>1):
				        stringList +="<h2>Instructional Textbooks</h2><ul>"
				    else:
				        stringList +="<h2>Instructional Textbook</h2><ul>"
				    while (len(InstructionalTextbook)>linkLength):
				        stringList+=InstructionalTextbook[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(InstructorsManual)>0):
				    if (len(InstructorsManual)>1):
				        stringList +="<h2>Instructor's Manuals</h2><ul>"
				    else:
				        stringList +="<h2>Instructor's Manual</h2><ul>"
				    while (len(InstructorsManual)>linkLength):
				        stringList+=InstructorsManual[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(MagazineTradePublication)>0):
				    if (len(MagazineTradePublication)>1):
				        stringList +="<h2>Magazine Trade Publications</h2><ul>"
				    else:
				        stringList +="<h2>Magazine Trade Publication</h2><ul>"
				    while (len(MagazineTradePublication)>linkLength):
				        stringList+=MagazineTradePublication[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Monographs)>0):
				    if (len(Monographs)>1):
				        stringList +="<h2>Monographs</h2><ul>"
				    else:
				        stringList +="<h2>Monograph</h2><ul>"
				    while (len(Monographs)>linkLength):
				        stringList+=Monographs[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Newsletter)>0):
				    if (len(Newsletter)>1):
				        stringList +="<h2>Newsletters</h2><ul>"
				    else:
				        stringList +="<h2>Newsletter</h2><ul>"
				    while (len(Newsletter)>linkLength):
				        stringList+=Newsletter[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Newspaper)>0):
				    if (len(Newspaper)>1):
				        stringList +="<h2>Newspapers</h2><ul>"
				    else:
				        stringList +="<h2>Newspaper</h2><ul>"
				    while (len(Newspaper)>linkLength):
				        stringList+=Newspaper[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(regularcolumn)>0):
				    if (len(regularcolumn)>1):
				        stringList +="<h2>Regular Column in Journal or Newspapers</h2><ul>"
				    else:
				        stringList +="<h2>Regular Column in Journal or Newspaper</h2><ul>"
				    while (len(regularcolumn)>linkLength):
				        stringList+=regularcolumn[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(ResearchReport)>0):
				    if (len(ResearchReport)>1):
				        stringList +="<h2>Research Reports</h2><ul>"
				    else:
				        stringList +="<h2>Research Report</h2><ul>"
				    f.write("<h2>Research Report</h2><ul>")
				    while (len(ResearchReport)>linkLength):
				        stringList+=ResearchReport[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(Software)>0):
				    if (len(Software)>1):
				        stringList +="<h2>Softwares</h2><ul>"
				    else:
				        stringList +="<h2>Software</h2><ul>"
				    while (len(Software)>linkLength):
				        stringList+=Software[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(StudyGuide)>0):
				    if (len(StudyGuide)>1):
				        stringList +="<h2>Study Guides</h2><ul>"
				    else:
				        stringList +="<h2>Study Guide</h2><ul>"
				    while (len(StudyGuide)>linkLength):
				        stringList+=StudyGuide[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(TechnicalReport)>0):
				    if (len(TechnicalReport)>1):
				        stringList +="<h2>Technical Reports</h2><ul>"
				    else:
				        stringList +="<h2>Technical Report</h2><ul>"
				    while (len(TechnicalReport)>linkLength):
				        stringList+=TechnicalReport[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(ArticleContainingCitation)>0):
				    if (len(ArticleContainingCitation)>1):
				        stringList +="<h2>Article's Containing Citation</h2><ul>"
				    else:
				        stringList +="<h2>Article's Containing Citatio</h2><ul>"
				    while (len(ArticleContainingCitation)>linkLength):
				        stringList+=ArticleContainingCitation[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
				linkLength = 0
				if (len(WorkingPaper)>0):
				    if (len(WorkingPaper)>1):
				        stringList +="<h2>Working Papers</h2><ul>"
				    else:
				        stringList +="<h2>Working Paper</h2><ul>"
				    while (len(WorkingPaper)>linkLength):
				        stringList+=WorkingPaper[linkLength].encode('ascii', 'ignore')
				        linkLength = linkLength+1
				    stringList+="</ul>"
			linkLength = 0
	    if hasPublication == False:
	        stringList = ""
	    self.publications = stringList
	    if "None" in self.publications:
			self.publications = self.publications.replace("None", "")
	    return self.publications

def testMethod(username, opener, rank, categories, catOnly):
	summary = ""
	directory = ""
	pciArray = []
	portal = getSite()
	form_folder = getattr(portal,'directory')
	#####form_folder = getattr(portal,'testdir')
	#####inner_folder = getattr(form_folder,'directory1')
	#####print username
	#####if hasattr(inner_folder,username) == False:
	if hasattr(form_folder,username) == False:
		p = Profiles2()
		pciArray = p.generatePCI(username, opener, rank, categories)
		bio = pciArray[0]
		summary = pciArray[1]
		temp = p.generateEducation(username, opener)
		summary = temp+summary
		directory +=p.generatePub(username, opener)
		directory +=p.generateConference(username, opener)
		directory +=p.generateGrants(username, opener)
		directory +=p.generateProf(username, opener)
		directory += p.generateAwards(username, opener)
		directory +=p.generateProfessionalMembership(username, opener)
		directory +=p.generateCertifications(username, opener)
		directory +=p.generateService(username, opener)
		if len(directory) > 0:
			directory ="<h1>Selected Publications and Accomplishments</h1>"+directory
		directory = temp+bio+directory
		directory+=p.resume
		create_plone_ProfilePage(p.fullname, username, directory, summary, catOnly, False)

def delObject(username):
    portal = getSite()
    #####folder = portal['testdir']
    #####del_item_folder = folder['directory1']
    folder = portal['directory']
    #####del_item_folder.manage_delObjects([username])
    folder.manage_delObjects([username])
    #####folder = portal['testdir']
    folder = portal['summary']
    #####del_item_folder = folder['summary1']
    #####del_item_folder.manage_delObjects([username+'-summary'])
    folder.manage_delObjects([username+'-summary'])

def update_profile(username = ""):
	newTab = False
	portal = getSite()
	summary = ""
	directory = ""
	#####if hasattr(portal, "testdir"):
	if hasattr(portal, "directory"):
		portal2 = getattr(portal,"directory")
		#####portal2 = getattr(portal,"testdir")
		#####if hasattr(portal2, 'directory1'):
			#####form_folder = getattr(portal2, 'directory1')
		if username == "":
			newTab = True
			username = portal2.portal_membership.getAuthenticatedMember().id
			#####username = form_folder.portal_membership.getAuthenticatedMember().id
		url = "http://www.uwosh.edu/cob/directory/"+username
		#####url = "http://www.uwosh.edu/cob/testdir/directory1/"+username
		#url = "http://localhost:8080/Plone/testdir/directory1/"+username
		#####print "username === "+username
		if username != "admin" and username != "acl_users":
			adminInfo = []
			#####start = time.time()
			opener = login()
			p = Profiles2()
			adminInfo = p.populate_admin(True,username, opener)
			categories = adminInfo[0]
			rank = adminInfo[1]
			catOnly = adminInfo[2]
			isActive = adminInfo[3]
			if isActive == True:
				pciArray = p.generatePCI(username, opener, rank, categories)
				bio = pciArray[0]
				summary = "<a class =\"summaryName\" href=\"http://www.uwosh.edu/cob/directory/"+username+"\">"+p.fullname+"</a>\n<br>"
				temp = p.generateEducation(username, opener)
				summary+=temp
				summary += pciArray[1]
				#temp = p.generateEducation(username, opener)
				#summary = temp+summary
				directory +=p.generatePub(username, opener)
				directory +=p.generateConference(username, opener)
				directory +=p.generateGrants(username, opener)
				directory +=p.generateProf(username, opener)
				directory += p.generateAwards(username, opener)
				directory +=p.generateProfessionalMembership(username, opener)
				directory +=p.generateCertifications(username, opener)
				directory +=p.generateService(username, opener)
				if len(directory) > 0:
					directory ="<h1>Selected Publications and Accomplishments</h1>"+directory
				directory = temp+bio+directory
				directory+=p.resume
				#####f = open('/Users/cobstu01/Desktop/iversen.html', 'w')
				#####f.write(directory)
				create_plone_ProfilePage(p.fullname,username, directory, summary, catOnly, True,)
			end = time.time()
			#####print "time is "+str(end-start)
			if newTab == True:
				new_tab(url)
			#####start = time.time()
			#####end = time.time()

def admin_update(username):
	exist = True
	returnInfo = []
	import webbrowser
	var = 2
	portal = getSite()
	summary = ""
	directory = ""
	#####if hasattr(portal, "testdir"):
		#####portal2 = getattr(portal,"testdir")
	if hasattr(portal, "directory"):
		portal2 = getattr(portal,"directory")
		#####if hasattr(portal2, 'directory1'):
			#####form_folder = getattr(portal2, 'directory1')
		url = "http://www.uwosh.edu/cob/directory/"+username
		#####url = "http://www.uwosh.edu/cob/testdir/directory1/"+username
		#url = "http://localhost:8080/Plone/testdir/directory1/"+username
		#####print "username === "+username
		if username != "admin" and username != "acl_users":
			adminInfo = []
			#####start = time.time()
			opener = login()
			p = Profiles2()
			adminInfo = p.populate_admin(True,username, opener)
			categories = adminInfo[0]
			rank = adminInfo[1]
			catOnly = adminInfo[2]
			isActive = adminInfo[3]
			if isActive == True:
				pciArray = p.generatePCI(username, opener, rank, categories)
				bio = pciArray[0]
				summary = "<a class =\"summaryName\" href=\"http://www.uwosh.edu/cob/directory/"+username+"\">"+p.fullname+"</a>\n<br>"
				temp = p.generateEducation(username, opener)
				summary+=temp
				summary+= pciArray[1]
				directory +=p.generatePub(username, opener)
				directory +=p.generateConference(username, opener)
				directory +=p.generateGrants(username, opener)
				directory +=p.generateProf(username, opener)
				directory += p.generateAwards(username, opener)
				directory +=p.generateProfessionalMembership(username, opener)
				directory +=p.generateCertifications(username, opener)
				directory +=p.generateService(username, opener)
				if len(directory) > 0:
					directory ="<h1>Selected Publications and Accomplishments</h1>"+directory
				directory = temp+bio+directory
				directory+=p.resume
				get_categories(username, p.fullname, catOnly)
			else:
				exist = False
			#####end = time.time()
			#####print str(end-start)
			#####start = time.time()
			#####end = time.time()
	return directory, summary, exist

def new_tab(url):
	import webbrowser
	from time import sleep
	webbrowser.open_new_tab(url)

def login():
    #####start = time.time()
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    username = "uwosh/fac_reports"
    top_level_url = "http://digitalmeasures.com/login/service/v4/SchemaData/INDIVIDUAL-ACTIVITIES-Business"
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    #####end = time.time()
    return opener

def get_categories(username, name, categories):
    portal = getSite()
    #####if hasattr(portal, "testdir"):
    	#####portal2 = getattr(portal, "testdir")
    	#####if hasattr(portal2, "directory1"):
	        #####form_folder = getattr(portal2, "directory1")
	        #####if hasattr(form_folder, username):
	            #####person = getattr(form_folder,username)
	            #####person.edit(subject=categories)
    	#####if hasattr(portal2, "summary1"):
		    #####form_folder = getattr(portal2, "summary1")
		    #####if hasattr(form_folder, username+"-summary"):
		        #####person = getattr(form_folder,username+"-summary")
		        #####person.edit(subject=categories)
    if hasattr(portal, "directory"):
		portal2 = getattr(portal, "directory")
    		if hasattr(portal2, username):
		        person = getattr(portal2,username)
		        person.edit(subject=categories)
		if hasattr(portal, "summary"):
		    form_folder = getattr(portal, "summary")
		    if hasattr(form_folder, username+"-summary"):
		        person = getattr(form_folder,username+"-summary")
		        person.edit(subject=categories)

##@param linkString
##A concatenated string
##This method is used to make sure that a string ends with a period. 
##It's not as simple as just checking the last character, because it could be in an order like (,.) or (..) or (.,)
def fixPuncuation(linkString):
    if(linkString[-1].isalpha() == True or linkString[-1].isdigit() == True or linkString[-1] == ")"):
            linkString = linkString+"."
            #####print "linkstring is ?"+linkString[-1]
#            return linkString
    elif linkString[-1] != "." or linkString[-1] != ")" or linkString[-1] != " " or linkString[-1] != ">":
        linkString = linkString.strip(linkString[-1])
        linkString = fixPuncuation(linkString)
    return linkString

#@param
##name
#@param username
##username of the faculty/staff member (part of the email before the @ symbol)
##@param userIdArray
## an array of all of the faculty/staff user Id's found in the xml files
#@param domPCI
#These are the XML doms for PCI, education, and Admin web services
#@param info
#HTML to be added to the profile page for a user.
def create_plone_ProfilePage(name, username, info, summary, categories, update):
	import glob
	i = 0
	j = 0
	portal = getSite()
	newProfile = False
	tempName = name
	if("'" in tempName):
	    tempName= tempName.replace("'","")
	else:
	    tempName = name
	tempName = tempName[:-5]
	username = username.lower()
	#####if hasattr(portal, "testdir"):
		#####portal2 = getattr(portal,"testdir")
		#####if hasattr(portal2, 'directory1'):
			#####form_folder = getattr(portal2, 'directory1')
			#####if hasattr(form_folder, username) == False:

	if hasattr(portal, "directory"):
		form_folder = getattr(portal,"directory")
		if hasattr(form_folder, username) == False:
			newProfile = True
		if update == False  or newProfile == True:
			tempPersonObject = form_folder.invokeFactory(type_name="Document", id= username, title = name)
			newItem = form_folder[tempPersonObject]
			newPage = getattr(form_folder, username)
			newPage.setExcludeFromNav(True)
			newPage.edit(subject=categories)
			newPage.edit('html',info)
		else:
			username = form_folder.portal_membership.getAuthenticatedMember().id
			if hasattr(form_folder, username):
				newPage = getattr(form_folder, username)
				newPage.setExcludeFromNav(True)
				newPage.edit(subject=categories)
				newPage.edit('html',info)
		if hasattr(portal, 'summary'):
			form_folder = getattr(portal, 'summary')
			if update == False or newProfile == True:
				tempPersonObject = form_folder.invokeFactory(type_name="Document", id= username+"-summary", title = name)
				newItem = form_folder[tempPersonObject]
				newPage = getattr(form_folder, username+"-summary")
				newPage.setExcludeFromNav(True)
				newPage.edit(subject=categories)
				newPage.edit('html',summary)
			else:
				username = form_folder.portal_membership.getAuthenticatedMember().id
				if hasattr(form_folder, username+"-summary"):
					newPage = getattr(form_folder, username+"-summary")
					newPage.setExcludeFromNav(True)
					newPage.edit(subject=categories)
					newPage.edit('html',summary)
def test():
	opener = login()
	p = Profiles2()
	p.populate_admin(False, "", opener)
