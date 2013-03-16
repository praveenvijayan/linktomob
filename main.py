#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import cgi
import urllib
import re
import random
import string
import settings
import time
import datetime

from google.appengine.ext import ndb
from google.appengine.api import mail
# from random import randint

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Greeting(ndb.Model):
	"""Models an individual Guestbook entry with content and date."""
	appcode = ndb.StringProperty()
	email = ndb.StringProperty()
	status = ndb.BooleanProperty()
	link = ndb.StringProperty()
	title = ndb.StringProperty()
	uniqueId = ndb.IntegerProperty(default=0)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def query_book(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.date)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template_values = {
            'greetings': "Greetings",
            'url': "url",
            'url_linktext': "link text",
        }
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

	def post(self):
		# self.response.out.write(self.request.get('email'))
		email = self.request.get('email')

		emailChk = UniqueIdGen().emailExist(email)
		emailVal = UniqueIdGen().emailValidation(email)
		 
		if emailChk:
			templatevalues = {
				'message':"Email already exist"
			}
			template = jinja_environment.get_template('error.html')
			self.response.out.write(template.render(templatevalues))
			return

		if emailVal and not email == '':

			# ancestor_key = ndb.Key("Email", email or "")
			# appcode = randint(1000,10000)
			appcode = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
			greeting = Greeting(appcode=appcode,email=email,status=False,link='',title='',uniqueId=0)
			greeting.put()
			
			template_values = {
				'email': email
			}

			template = jinja_environment.get_template('success.html')
			self.response.out.write(template.render(template_values))
			link = settings.LINKTOMOB + "reg?appcode=" +appcode +"&email=" + email

			emailTpl_values = {
				'link':link
			}

			emailTpl = jinja_environment.get_template('email.html')
			emailContent = emailTpl.render(emailTpl_values)

			# self.response.out.write(emailTpl);

			# mail.send_mail(sender="Link to mobile <praveenv.vijayan@gmail.com>",
	              # to=email,
	              # subject="Link to Mobile :: Your account has been approved",
	              # body.html=emailContent)
			message = mail.EmailMessage(sender="Link to mobile <praveenv.vijayan@gmail.com>",
                            subject="Link to Mobile :: Your account has been approved")
			message.to = email

			message.body = """
			
			"""

			message.html = emailContent
			
			message.send()

		else:
			templatevalues = {
				'message':"Invalid email"
			}
			template = jinja_environment.get_template('error.html')
			self.response.out.write(template.render(templatevalues))


class RegHandler(webapp2.RequestHandler):
	def get(self):
		# self.response.out.write("Test")
		appcode = self.request.get('appcode')
		email = self.request.get('email')
		uId = UniqueIdGen()
		slNos = Greeting.query(Greeting.appcode == appcode)
		for slno in slNos:
			if slno.email == email:
				# self.response.out.write(uId.genId())
				if slno.status == True:
					# self.response.out.write("Already Activated and your id %s " % slno.uniqueId)
					templatevalues = {
						'message':"This mail is already activated!!",
						'hide':'hide'
					}
					template = jinja_environment.get_template('error.html')
					self.response.out.write(template.render(templatevalues))

				else:
					update = slNos.get()
					update.status = True
					update.uniqueId = uId.genId()
					update.link = settings.PLACEHOLDER_DOMAIN
					update.put()

					template_values = {
						'code': update.uniqueId,
						'email':email
					}

					template = jinja_environment.get_template('reg.html')
					self.response.out.write(template.render(template_values))

			else:
				template_values = {
					'message':"Invalid application code or email ID!",
					'hide':'hide',
					'class':'invalid-code'
				}
				template = jinja_environment.get_template('error.html')
				self.response.out.write(template.render(template_values))

		

class UrlHandler(webapp2.RequestHandler):
	def get(self, user_id):
		# self.response.out.write("URL Handler %s" %     )
		url = self.request.get('url')
		email=self.request.get('email')
		title=self.request.get('title')
		slNos = Greeting.query(Greeting.uniqueId == int(user_id))
		emailChk = UniqueIdGen().emailExist(email)	

		if not url:		
			allItem = slNos.order(-Greeting.date)
			self.redirect("%s" % str(allItem.get().link))
			# allItem = slNos.fetch()
			# self.response.out.write(allItem.get().link)
			# for slno in slNos:
				# self.response.out.write(slno.link)
				# self.redirect("%s" % str(slno.link))
		else:
			if emailChk:
				linkUpdate = slNos.get()
				
				for slno in slNos:
					if slno.link == url:
						# template_values = {
						# 	'message':"Url already exists!",
						# 	'hide':'hide'
						# }
						# template = jinja_environment.get_template('error.html')
						# self.response.out.write(template.render(template_values))
						slno.date = datetime.datetime.now()
						slno.put()
						self.redirect("%s"% str(url))
						return
				
				if not settings.PLACEHOLDER_DOMAIN == linkUpdate.link:
					appcode = UniqueIdGen().getAppcode(email)
					uid = UniqueIdGen().getUid(email)
					greeting = Greeting(appcode=appcode,email=email,status=True,link=url,title=title,uniqueId=uid)
					greeting.put()
				else:
					linkUpdate.link = url
					linkUpdate.title = title
					linkUpdate.put()
				
					# linkUpdate = slNos.get()
					# linkUpdate.link = url
					# linkUpdate.title = title
					# linkUpdate.put()

					# greeting = Greeting(appcode=appcode,email=email,status=False,link='',title='',uniqueId=0)
					# greeting.put()

				template = jinja_environment.get_template('add.html')
				self.response.out.write(template.render())
				self.redirect("%s"% str(url))

class UrlShow(webapp2.RequestHandler):
	def get(self, user_id, page):

		if int(page) <= 0:
			template_values ={
				"message":"Please enter a number more than zero!",
				"hide":"hide",
				"class":"error-block"
			}
			template = jinja_environment.get_template('error.html')
			self.response.out.write(template.render(template_values))
			return

		greetings = Greeting.query(Greeting.uniqueId == int(user_id)).order(-Greeting.date).fetch(int(page))
		 
		template_values = {
			'greetings':greetings
		}

		template = jinja_environment.get_template('list.html')
		self.response.out.write(template.render(template_values))

class Bookmark(webapp2.RequestHandler):
	def get(self, user_id):
		# appcode = self.request.get('appcode')
		# email = self.request.get('email')
		userEmail = Greeting.query(Greeting.uniqueId == int(user_id))

		template_values = {
			'code':user_id,
			'email':userEmail.get().email
		}
		template = jinja_environment.get_template('bookmarklet.html')
		self.response.out.write(template.render(template_values))

class UniqueIdGen(webapp2.RequestHandler):
	def genId(self):
		uIds = Greeting.query(Greeting.status == True).count()
		return uIds+1

	def emailExist(self, email):
		email = Greeting.query(Greeting.email == email).count()
		if email > 0:
			return True
		else:
			return False

	def emailValidation(self, email):
		if re.match(r"[^@]+@[^@]+\.[^@]+", email):
			return True
		else:
			return False

	def getAppcode(self,email):
		appCodes = Greeting.query(Greeting.email == email)
		for appcode in appCodes:
			return appcode.appcode

	def getUid(self,email):
		uIds = Greeting.query(Greeting.email == email)
		for uid in uIds:
			return uid.uniqueId


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/reg', RegHandler),
    ('/(\d+)', UrlHandler),
    ('/(\d+):(\d+)', UrlShow),
    ('/(\d+)/bookmark', Bookmark)
], debug=True)
