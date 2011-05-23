import uri
import re
from random import Random
import string 

def randString():
	return ''.join( Random().sample(string.letters, 6))
		
def getAllForms(soup):
	return soup.findAll('form',action=True,method=re.compile("post", re.IGNORECASE))

class Form():
	def prepareFormInputs(self, form):
		"create inputs from a form"
		input = {}
		#Process <input type="test" name="...
		for m in form.findAll('input',{'name' : True,'type' : 'text'}):
			if re.search(' value=',m.__str__()):
				value=m['value'].encode('utf8')
			else:
				value=randString()
			input[m['name']] = value
		#Process <input type="password" name="...
		for m in form.findAll('input',{'name' : True,'type' : 'password'}):
			if re.search(' value=',m.__str__()):
				value=m['value'].encode('utf8')
			else:
				value=randString()
			input[m['name']] = value
		#Process <input type="submit" name="...
		for m in form.findAll('input',{'name' : True,'type' : 'submit'}):
			if re.search(' value=',m.__str__()):
				value=m['value'].encode('utf8')
			else:
				value=randString()
			input[m['name']] = value
		#Process <input type="hidden" name="...
		for m in form.findAll('input',{'name' : True,'type' : 'hidden'}):
			if re.search(' value=',m.__str__()):
				value=m['value'].encode('utf8')
			else:
				value=randString()
			input[m['name']] = value
		#Process <input type="checkbox" name="...
		for m in form.findAll('input',{'name' : True,'type' : 'checkbox'}):
			if re.search(' value=',m.__str__()):
				value=m['value'].encode('utf8')
			else:
				value=randString()
			input[m['name']] = value
		#Process <input type="radio" name="...
		listRadio = []
		for m in form.findAll('input',{'name' : True,'type' : 'radio'}):
			if (not m['name'] in listRadio) and re.search(' value=',m.__str__()):
				listRadio.append(m['name'])
				input[m['name']] = value.encode('utf8')
		#Process <textarea name="...
		for m in form.findAll('textarea',{'name' : True}):
			if len(m.contents)==0:
				m.contents.append(randString())
			input[m['name']] = m.contents[0].encode('utf8')
		#Process <select name="...
		for m in form.findAll('select',{'name' : True}):
			if len(m.findAll('option',value=True))>0:
				name = m['name']
				input[name] = m.findAll('option',value=True)[0]['value'].encode('utf8')
		return input