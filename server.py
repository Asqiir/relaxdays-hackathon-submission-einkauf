#docker build -t einkauf .
#docker run -p 8080:8080 einkauf

from bottle import request, response, run, post, get, put, delete, route
import json
import yaml
import datetime
from Levenshtein import distance



def convert_to_en_format(x): #assumes %d.%m.%Y %H:%M:%S input, returns %Y.%m.%d %H:%M:%S output
	return x[6:10] + '-' + x[3:5] + '-' + x[0:2] + ' ' + x[11:19]


class Verwalter:
	data = []
	json_file = 'data.json'

	def __init__(self):
		self.__write()

	def __sort(self):
		self.data_sorted_by_date = sorted(self.data, key=lambda k:k['time'])

	def __write(self):
		with open(self.json_file,'w') as file:
			file.write(json.dumps(self.data))

	def add(self,einkauf):
		einkauf['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.data.append(einkauf)
		self.__write()

	def getAll(self,article_id=None):
		if article_id is None:
			return self.data
		else:
			return list(filter(lambda k:k['articleID']==article_id, self.data))

	def getByDate(self, after=None, before=None):
		return list(filter(lambda k:(after==None or after<=k['time']) and (before==None or before>=k['time']), self.data))

	def getLieferanten(self):
		l = set()
		for entry in self.data:
			l.add(entry['lieferant'])
		return l

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

@get('/searchLieferant')
def searchLieferant():
	search = request.query['x']
	response.headers['Content-Type'] = 'application/json'
	lieferanten = verwalter.getLieferanten()
	levenshtein = dict()

	#calc once
	for l in lieferanten:
		levenshtein[l]=distance(search,l)

	#filter
	levenshtein = {k: v for (k, v) in levenshtein.items() if v<=10}

	#sort
	lieferanten = sorted(levenshtein.keys(), key=lambda k:levenshtein[k])


	return json.dumps(lieferanten)


@get('/purchasesBetween')
def purchasesBetween():
	x = request.query['x']
	y = request.query['y']

	x_en = convert_to_en_format(x)
	y_en = convert_to_en_format(y)

	return json.dumps(verwalter.getByDate(after=x_en,before=y_en))


global swagger_json
swagger_json = None
with open('swagger.yaml') as file:
	swagger_json = yaml.safe_load(file)

@route('/swagger')
def swagger():
	return swagger_json




run(host='0.0.0.0', port=8080)
