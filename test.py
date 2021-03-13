import requests
import json

def compare_lists(list1, list2): 
    return sorted(list1, key=lambda k:(k['lieferant'],k['articleID'],k['menge']))==sorted(list2, key=lambda k:(k['lieferant'],k['articleID'],k['menge']))

o1 = {'lieferant':'x','articleID':3,'menge':10}
o2 = {'lieferant':'x','articleID':3,'menge':10}
o3 = {'lieferant':'y','articleID':3,'menge':10}
o4 = {'lieferant':'x','articleID':7,'menge':10}

requests.post("http://0.0.0.0:8080/purchase", data=json.dumps(o1))
requests.post("http://0.0.0.0:8080/purchase", data=json.dumps(o2))
requests.post("http://0.0.0.0:8080/purchase", data=json.dumps(o3))
requests.post("http://0.0.0.0:8080/purchase", data=json.dumps(o4))

with open('data.json','r') as file:
	data = json.loads(file.read())
	if not compare_lists(data, [o1,o2,o3,o4]):
		print(data)
		print('POST wrong')

r = requests.get("http://0.0.0.0:8080/purchases")

with open('data.json','r') as file:
	data = r.json()
	if not compare_lists(data, [o1,o2,o3,o4]):
		print(data)
		print('GET ALL wrong')

r1 = requests.get("http://0.0.0.0:8080/purchaseForArticle", params={'x':3})
r2 = requests.get("http://0.0.0.0:8080/purchaseForArticle", params={'x':7})
r3 = requests.get("http://0.0.0.0:8080/purchaseForArticle", params={'x':0})

with open('data.json','r') as file:
	data = r1.json()
	if not compare_lists(data, [o1,o2,o3]):
		print(data)
		print('GET ALL 1 wrong')
	data = r2.json()
	if not compare_lists(data, [o4]):
		print(data)
		print('GET ALL 2 wrong')
	data = r3.json()
	if not compare_lists(data, []):
		print(data)
		print('GET ALL 3 wrong')