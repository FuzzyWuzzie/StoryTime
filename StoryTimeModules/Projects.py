import cherrypy

class Projects(object):
	exposed = True

	def __init__(self, sql):
		super(Projects, self).__init__()
		self.sql = sql

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, listAll=0):
		if listAll == 0:
			# deal with sessions
			if 'projid' not in cherrypy.session:
				cherrypy.session['projid'] = 1
				cherrypy.session['projname'] = 'Test'

			# tell the user their current session
			return {
				'projid': cherrypy.session['projid'],
				'projname': cherrypy.session['projname']
			}
		else:
			projects = []
			for projid, name in self.sql.select('select projid, name from projects order by name asc'):
				projects.extend([{
					'projid': projid,
					'projname': name
				}])
			return projects

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def POST(self, projid):
		projid = int(projid)
		if projid == -1:
			# clear the project id
			cherrypy.session['projid'] = None
			cherrypy.session['projname'] = None

			return {
				'result': 'success'
			}
		else:
			# get the name associated with this project id
			projname = None
			for name in self.sql.select('select name from projects where projid=? limit 1;', [projid]):
				projname = name

			if projname is None:
				raise cherrypy.HTTPError(404, 'That project id does not exist!')

			cherrypy.session['projid'] = projid
			cherrypy.session['projname'] = projname

			return {
				'result': 'success',
				'projid': projid,
				'projname': projname
			}

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def PUT(self, projname):
		# insert it!
		self.sql.execute('insert into projects(name) values(?)', [projname])
		print('PUTTING new project: ' + projname)

		return {
			'result': 'success'
		}

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def DELETE(self, projid):
		# delete it
		self.sql.execute('delete from projects where projid=?', [projid])
		return {
			'result': 'success'
		}