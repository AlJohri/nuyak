from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nuyak.firebaseio.com', None)
yaks = firebase.get("/yaks", None)

import unicodecsv as csv

with open("yaks.csv", "w") as f:
	writer = csv.writer(f)
	writer.writerow(['id', 'message'])
	for message_id, yak in yaks.iteritems():
		if message_id == "Y": continue
		writer.writerow([message_id, yak.get('message')])
