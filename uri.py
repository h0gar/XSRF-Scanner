import urlparse
import re

#class URI():
def buildUrl(url, href):
	"build a new uri from url to href"
	#should replace it with exclusion list
	if re.search('logout',href) or re.search('action=out',href) or re.search('action=logoff', href) or re.search('action=delete',href) or re.search('UserLogout',href) or re.search('osCsid', href) or re.search('file_manager.php',href) or href=="http://localhost":#make exclusion list
		return ''
	
	parsed = urlparse.urlsplit(href)
	app=''
	#if url & href have same domain
	if parsed[1] == urlparse.urlsplit(url)[1]:
		app=href
	else:
		#destination uri has no domain
		if len(parsed[1]) == 0 and (len(parsed[2]) != 0 or len(parsed[3])!=0):
			domain = urlparse.urlsplit(url)[1]
			#if destination uri starts with /
			if re.match('/', parsed[2]):
				app = 'http://' + domain + parsed[2]
				if parsed[3]!='':
					app += '?'+parsed[3]
			else:
				try:
					app = 'http://' + domain + re.findall('(.*\/)[^\/]*', urlparse.urlsplit(url)[2])[0] + parsed[2]
				except IndexError:
					app = 'http://' + domain + parsed[2]
				if parsed[3]!='':
					app += '?'+parsed[3]
	#return '' for invalid url, url otherwise
	return app

def buildAction(url, action):
	"create an action uri from current location and destination"
	if action!='' and not re.match('#',action):
		return buildUrl(url,action)
	else:
		return url