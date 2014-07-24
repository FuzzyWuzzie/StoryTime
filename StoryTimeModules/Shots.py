import cherrypy
import os

class Shots(object):
	exposed = True

	def __init__(self, sql):
		super(Shots, self).__init__()
		self.sql = sql

	def updateShots(self):
		self.shots = []
		for shotid, project, index, title, img, notes in self.sql.select('select shotid, project, shotOrder, title, img, notes from shots where project=? order by shotOrder asc, project asc', [cherrypy.session['projid']]):
			shot = {
				'id': int(shotid),
				'index': int(index),
				'title': title,
				'img': img,
				'notes': notes
			}
			self.shots.extend([shot])

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def GET(self, shotID=-1):
		self.updateShots()
		if len(self.shots) == 0:
			return [{
				'id': -1
			}]
		if shotID == -1:
			# sort the shots
			self.shots = sorted(self.shots, key=lambda item: item['index'])
			return self.shots
		else:
			for shot in self.shots:
				if shot['id'] == int(shotID):
					return shot
			return {}

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def POST(self, shotID, field, value):
		shotID = int(shotID)
		for i in range(0, len(self.shots)):
			if shotID == self.shots[i]['id']:
				if field == 'notes':
					self.shots[i]['notes'] = value
					self.sql.execute('update shots set notes=? where shotid=?', [value, shotID])
					return self.shots[i]
				elif field == 'index':
					self.shots[i]['index'] = int(value)
					self.sql.execute('update shots set shotOrder=? where shotid=?', [int(value), shotID])
					return self.shots[i]
				elif field == 'title':
					self.shots[i]['title'] = value
					self.sql.execute('update shots set title=? where shotid=?', [value, shotID])
					return self.shots[i]
				else:
					return "Error: Unsupported field!"
		return "Error: ID not found!"

	def getNameWithoutExtension(self, path):
		return os.path.splitext(os.path.basename(path))[0]

	def getExtension(self, path):
		return os.path.splitext(path)[1]

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def PUT(self, newShotTitle, newShotImage, newShotNotes, newShotProject, newShotIndex, newShotIndexTarget):
		# upload the file
		size = 0
		allData = bytes()
		while True:
			data = newShotImage.file.read(8192)
			if not data:
				break
			allData += data
			size += len(data)

		# calculate the new filename
		files = os.listdir('template/img');
		highestInt = 0;
		for file in files:
			withoutExt = self.getNameWithoutExtension('template/img/' + file)
			try:
				if int(withoutExt) > highestInt:
					highestInt = int(withoutExt)
			except:
				pass

		extension = self.getExtension(newShotImage.filename)
		fileName = 'template/img/%06d%s' % (highestInt + 1, extension)
		url = '/img/%06d%s' % (highestInt + 1, extension)

		savedFile = open(fileName, 'wb')
		savedFile.write(allData)
		savedFile.close()

		# change the index of all the other records
		newShotIndex = int(newShotIndex)
		if newShotIndex == -1:
			# there is no key to reference, so put it at the start
			newShotIndex = 0
		else:
			# get the index of the selected node
			for row in self.sql.select('select shotOrder from shots where shotid=?', [newShotIndex]):
				newShotIndex = row[0]

		# insert it somewhere
		newShotIndex = float(newShotIndex)
		print('')
		print('target shot index: %f' % newShotIndex)
		if newShotIndexTarget == 'after':
			newShotIndex += 0.5
		else:
			newShotIndex -= 0.5
		print('new shot index: %f' % newShotIndex)
		#self.sql.execute('update shots set shotOrder = shotOrder + 1 where shotOrder %s ? and project = ?' % sign, [newShotIndex, cherrypy.session['projid']])

		# now update the records
		self.sql.execute('insert into shots(project, shotOrder, title, img, notes) values(?, ?, ?, ?, ?)', [cherrypy.session['projid'], newShotIndex, newShotTitle, url, newShotNotes])

		# now update all the records
		i = 0.0
		for shot in self.sql.select('select shotid from shots where project=? order by shotOrder asc', [cherrypy.session['projid']]):
			print('shotid %d set to order %f' % (int(shot[0]), i))
			self.sql.execute('update shots set shotOrder=? where shotid=?', [i, shot[0]])
			i += 1.0
		print('')

		# and get that record
		shotID = None
		for newShotID in self.sql.select('select shotid from shots order by shotid desc limit 1'):
			shotID = int(newShotID[0])

		# and return a result
		return {
			'result': 'success',
			'id': shotID,
			'title': newShotTitle,
			'img': url,
			'notes': newShotNotes
		}

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def DELETE(self, shotID):
		shotID = int(shotID)

		# delete it
		self.sql.execute('delete from shots where shotid=?', [shotID])

		# and update the shots
		self.updateShots()

		return {
			'result': 'success'
		}