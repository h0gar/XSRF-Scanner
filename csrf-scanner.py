#!/usr/bin/env python

# TO DO #
'''
-make an exclusion list
-give an option for breaks
-form GET
(-avoid scanning URIs like ?id=1 and ?id=2)
-actionDone ?
-preciser type de http error
-auto-relogin
-soucis headers
-find where xsrf error message
-make something for link rules
'''

# IMPORT #

import difflib
import cookielib
import urlparse
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import mechanize
import re
import Crawler
import Form
import uri

import time

def request(referer,action,form,opener):
	"Sends a HTTP POST request"
	data = urllib.urlencode(form)
	#try:
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)','Referer' : referer}
	#opener.addheaders = [('Referer',referer)]
	try:
		return opener.open(action,data).read()
	except:
		return ''
	'''except urllib2.HTTPError:
		print "HTTP Error 1: "+action
		return
	except ValueError:
		print "Value Error: "+action
		return'''




# Main
user1Cookie = cookielib.CookieJar() #initialize user 1 cookie jar
user2Cookie = cookielib.CookieJar() #initialize user 2 cookie jar
opener1 = urllib2.build_opener(urllib2.HTTPCookieProcessor(user1Cookie)) #initialize user 1 opener
opener2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(user2Cookie)) #initialize user 2 opener

#visited form
actionDone = []

#detect csrf
csrf=''#r'(Invalid Token|voir cette ressource|Identifiant)'
#login process
#start='http://www.google.com'
root='http://www.aalto.fr/'
start = root
form1="""<form action="/drupal/?q=node&amp;destination=node"  accept-charset="UTF-8" method="post" id="user-login-form"> 
<div><div class="form-item" id="edit-name-wrapper"> 
 <label for="edit-name">Username: <span class="form-required" title="This field is required.">*</span></label> 
 <input type="text" maxlength="60" name="name" id="edit-name" size="15" value="test1" class="form-text required" /> 
</div> 
<div class="form-item" id="edit-pass-wrapper"> 
 <label for="edit-pass">Password: <span class="form-required" title="This field is required.">*</span></label> 
 <input type="password" value="a9z8e7" name="pass" id="edit-pass"  maxlength="60"  size="15"  class="form-text required" /> 
</div> 
<input type="submit" name="op" id="edit-submit" value="Log in"  class="form-submit" /> 
<div class="item-list"><ul><li class="first"><a href="/drupal/?q=user/register" title="Create a new user account.">Create new account</a></li> 
<li class="last"><a href="/drupal/?q=user/password" title="Request new password via e-mail.">Request new password</a></li> 
</ul></div><input type="hidden" name="form_build_id" id="form-6a060c0861888b7321fab4f5ac6cb908" value="form-6a060c0861888b7321fab4f5ac6cb908"  /> 
<input type="hidden" name="form_id" id="edit-user-login-block" value="user_login_block"  /> 
</div></form> """

form2="""<form action="/drupal/?q=node&amp;destination=node"  accept-charset="UTF-8" method="post" id="user-login-form"> 
<div><div class="form-item" id="edit-name-wrapper"> 
 <label for="edit-name">Username: <span class="form-required" title="This field is required.">*</span></label> 
 <input type="text" maxlength="60" name="name" id="edit-name" size="15" value="test2" class="form-text required" /> 
</div> 
<div class="form-item" id="edit-pass-wrapper"> 
 <label for="edit-pass">Password: <span class="form-required" title="This field is required.">*</span></label> 
 <input type="password" value="a9z8e7" name="pass" id="edit-pass"  maxlength="60"  size="15"  class="form-text required" /> 
</div> 
<input type="submit" name="op" id="edit-submit" value="Log in"  class="form-submit" /> 
<div class="item-list"><ul><li class="first"><a href="/drupal/?q=user/register" title="Create a new user account.">Create new account</a></li> 
<li class="last"><a href="/drupal/?q=user/password" title="Request new password via e-mail.">Request new password</a></li> 
</ul></div><input type="hidden" name="form_build_id" id="form-6a060c0861888b7321fab4f5ac6cb908" value="form-6a060c0861888b7321fab4f5ac6cb908"  /> 
<input type="hidden" name="form_id" id="edit-user-login-block" value="user_login_block"  /> 
</div></form> """

form = Form.Form()
bs1=BeautifulSoup(form1).findAll('form',action=True)[0]
bs2=BeautifulSoup(form2).findAll('form',action=True)[0]
#action = uri.buildAction(start,bs1['action'])
action = start
#opener1.open(action,urllib.urlencode(form.prepareFormInputs(bs1)))
#opener2.open(action,urllib.urlencode(form.prepareFormInputs(bs2)))
opener1.open(action)
opener2.open(action)

crawler = Crawler.Crawler(start,opener1)
print "Scanning..."
try:
	#for each url in queue
	while crawler.hasNext():
		url = crawler.next()

		print url	#display current url
		
		soup=crawler.process(root)
		if not soup:
			continue;
		
		# Process page's forms #
		i=0
		for m in  Form.getAllForms(soup):	#take all forms wich have action attribute
			action = uri.buildAction(url,m['action'])
			if not action in actionDone and action!='':
				try:
					formResults=form.prepareFormInputs(m)	#get inputs for form m
					r1 = request(url,action,formResults,opener1)	#send request with user1
					formResults=form.prepareFormInputs(m)	#regenerate data
					r2 = request(url,action,formResults,opener2)	#send same request with user 2
					if(len(csrf)>0):
						if not re.search(csrf, r2):
							#We got a CSRF!
							try:
								print '=CSRF='+"\n\t"+'Name: '+m['name']+"\n\t"+'Action: '+m['action']+"\n\t"+'From: '+url+"\n"
							except KeyError:
								print '=CSRF='+"\n\t"+'Action: '+m['action']+"\n\t"+'From: '+url
							print "\t"+urllib.urlencode(formResults)
						continue;
					o2 = opener2.open(url).read()	#user 2 gets his own form
					try:
						form2 = Form.getAllForms(BeautifulSoup(o2))[i]	#retrieve the same form as user 1
					except IndexError:
						print 'Form Error'
						continue;
					#user 2 sends his own request
					contents2 = form.prepareFormInputs(form2)
					r3 = request(url,action,contents2,opener2)

					diffr1r2 = difflib.ndiff(r1.splitlines(1),r2.splitlines(1))	#look up differences between r1 & r2
					diffr1r3 = difflib.ndiff(r1.splitlines(1),r3.splitlines(1))	#look up differences between r1 & r3

					#Keep only +|- differences
					resultr1r2 = []
					for n in diffr1r2:
						if re.match('\+|-',n):
							resultr1r2.append(n)
					resultr1r3 = []
					for n in diffr1r3:
						if re.match('\+|-',n):
							resultr1r3.append(n)

					#if the number of differences between r1/r2 is smaller than between r1/r3
					if len(resultr1r2)<=len(resultr1r3):
						#We got a CSRF! Or not.
						try:
							print '=CSRF='+"\n\t"+'Name: '+m['name']+"\n\t"+'Action: '+m['action']+"\n\t"+'From: '+url+"\n"
						except KeyError:
							print '=CSRF='+"\n\t"+'Action: '+m['action']+"\n\t"+'From: '+url
						print "\t"+urllib.urlencode(formResults)
						
				except urllib2.HTTPError, msg:
					print msg.__str__()
					pass
			actionDone.append(action)
			i+=1
	print "Scan completed!"
except KeyboardInterrupt:
	pass
except KeyboardInterrupt:
	print "\n= To Visit ="
	for i in crawler.getToVisit():
		print i
	print "\n= Visited ="
	for i in crawler.getVisited():
		print i
	print "\nInterrupted by user"
