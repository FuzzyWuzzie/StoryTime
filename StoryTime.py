import sys
import cherrypy
from cherrypy.lib import auth_digest
import hashlib
import os
import win32serviceutil
import win32service
import logging
from MultiThreadSQLite import MultiThreadSQLite
from StoryTimeModules.Shots import Shots
from StoryTimeModules.Upload import FileUpload
from StoryTimeModules.Projects import Projects

class DocBot(object):
	def __init__(self, sql):
		super(DocBot, self).__init__()
		self.sql = sql

		self.shots = Shots(sql)
		self.upload = FileUpload(sql)
		self.projects = Projects(sql)

		cherrypy.engine.subscribe('stop', self.stop)

	@cherrypy.expose
	def index(self):
		html = ""

		# deal with sessions
		if 'projid' not in cherrypy.session or cherrypy.session['projid'] is None:
			# open the project selection file
			with open('template/selectProject.html', 'r') as templateFile:
				html = templateFile.read()

		else:
			# open the template file
			with open('template/index.html', 'r') as templateFile:
				html = templateFile.read()

			# place the modals into the template
			modals = ""
			modalFiles = os.listdir('template/modals')
			for fileName in modalFiles:
				with open('template/modals/%s' % fileName, 'r') as modalFile:
					modal = modalFile.read()
					modals += modal
			html = html.replace("{{ modals }}", modals)

		# and return the templated file
		return html

	@cherrypy.expose
	def logout(self):
		html = ""
		with open('template/loggedOut.html', 'r') as templateFile:
			html = templateFile.read()

		cherrypy.response.status = 401
		return html
		#raise cherrypy.HTTPError(401, html)

	def error_page_404(status, message, traceback, version):
		return "Nothing to see here!"
	cherrypy.config.update({'error_page.404': error_page_404})

	#def error_page_401(status, message, traceback, version):
	#	return message
	#cherrypy.config.update({'error_page.401': error_page_401})

	def stop(self):
		self.sql.close()

if __name__ == '__main__':
	# load the database
	sql = MultiThreadSQLite('stories.db')

	# load the users from the database
	users = {}
	ret = sql.select('select name, secret from users')
	for user in ret:
		users[user[0]] = user[1]

	# setup the cherrypy configuration
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.server.socket_port = 9090
	conf = {
		'/': {
			'tools.auth_digest.on': True,
			'tools.auth_digest.realm': 'localhost',
			'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict(users),
			'tools.auth_digest.key': 'Time for stories!',
			'tools.staticdir.root': os.path.abspath(os.getcwd()),
			'tools.sessions.on': True,
		},
		'/css': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join('template', 'css')
		},
		'/js': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join('template', 'js')
		},
		'/fonts': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join('template', 'fonts')
		},
		'/img': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join('template', 'img')
		},
		'/shots': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
		},
		'/upload': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
		},
		'/projects': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
		},
	}

	# disable auto-reload
	cherrypy.config.update({'engine.autoreload.on': False})

	# initialize the server
	app = DocBot(sql)

	# start the server
	cherrypy.quickstart(app, '/', conf)