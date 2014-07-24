import os
import cherrypy
from cherrypy.lib import static

class FileUpload(object):
	exposed = True

	def __init__(self, sql):
		super(FileUpload, self).__init__()
		self.sql = sql

	def getNameWithoutExtension(self, path):
		return os.path.splitext(os.path.basename(path))[0]

	def getExtension(self, path):
		return os.path.splitext(path)[1]

	@cherrypy.tools.accept(media='text/plain')
	@cherrypy.tools.json_out()
	def POST(self, shotID, uploadedFile):
		shotID = int(shotID)
		size = 0
		allData = bytes()
		while True:
			data = uploadedFile.file.read(8192)
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

		extension = self.getExtension(uploadedFile.filename)
		fileName = 'template/img/%06d%s' % (highestInt + 1, extension)
		url = '/img/%06d%s' % (highestInt + 1, extension)

		savedFile = open(fileName, 'wb')
		savedFile.write(allData)
		savedFile.close()

		# and update the SQL
		self.sql.execute('update shots set img=? where shotid=?', [url, shotID])

		return {
			'name': os.path.basename(fileName),
			'size': size,
			'url': url,
		}
