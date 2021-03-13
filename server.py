#docker build -t einkauf .
#docker run -p 8080:8080 einkauf

from bottle import request, response, run, post, get, put, delete
import json

class Verwalter:
	data = []
	json_file = 'data.json'

	def __init__(self):
		self.__write()

	def __write(self):
		with open(self.json_file,'w') as file:
			file.write(json.dumps(self.data))

	def add(self,einkauf):
		self.data.append(einkauf)
		self.__write()

	def getAll(self,article_id=None):
		if article_id is None:
			return self.data
		else:
			return list(filter(lambda k:k['articleID']==article_id, self.data))

verwalter=Verwalter()

@get('/purchases')
def purchases():
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(verwalter.getAll())

@post('/purchase')
def purchase():
	einkauf = json.loads(request.body.read().decode('utf-8'))
	verwalter.add(einkauf)
	return 'done'

@get('/purchaseForArticle')
def purchaseForArticle():
	articleID = int(request.query['x'])
	response.headers['Content-Type'] = 'application/json'
	return json.dumps(verwalter.getAll(article_id=articleID))


run(host='0.0.0.0', port=8080)