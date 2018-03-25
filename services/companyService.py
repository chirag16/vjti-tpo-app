from flask import *
import json
import os
app = Flask(__name__)

JSON_DB_PATH = '../database'
USER_DB_NAME = 'users.json'
INVITED_COMPANY_DB_NAME = 'invited.json'
SCHEDULE_DB_NAME = 'schedule.json'
APPLICATIONS_PATH = '../database/applications.json'

invited = []
schedule = []
users = []

with open(os.path.join(JSON_DB_PATH, USER_DB_NAME), "r") as db:
	users = json.load(db)

with open(os.path.join(JSON_DB_PATH, INVITED_COMPANY_DB_NAME), "r") as db:
	invited = json.load(db)

with open(os.path.join(JSON_DB_PATH, SCHEDULE_DB_NAME), "r") as db:
	schedule = json.load(db)

students = users["students"]
companies = users["companies"]

def addToInvited(companyDetails):
	global invited
	invited["companies"].append(companyDetails)
	with open(os.path.join(JSON_DB_PATH, INVITED_COMPANY_DB_NAME), "w") as db:
		json.dump(invited, db)

@app.route('/sendRequestToTpo')
def new_request():
	return render_template('sendRequestToTpo1.html')

@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		try:			
			addToInvited({u"employmentType": request.form["employment"], u"id": request.form["id"], u"name": request.form["name"]})

			msg = "Record inserted"
		except Exception as e:
			msg = "Error in insertion"
		finally:
			return render_template('resultSendRequestToTpo.html', msg = msg)
			# con.close()
	return 'OK'

@app.route('/sendShortList')
def req():
	return render_template('sendShortList1.html')

@app.route('/update', methods = ['POST', 'GET'])
def update():
	if request.method == 'POST':
		msg = "-"
		try:			
			with open(APPLICATIONS_PATH, 'r') as f:
				applications = json.load(f)
			for i in range(len(applications['entries'])):
				if applications['entries'][i]['name'] == request.form['name'] and applications['entries'][i]['company'] == request.form['company']:
					applications['entries'][i]['status'] = request.form['status']
			with open(APPLICATIONS_PATH, 'w') as f:
				json.dump(applications, f)

			msg = "Record inserted"
		except Exception as e:
			print e
			msg = "Error in insertion"
		finally:
			return render_template('resultSendShortList.html', msg = msg)
			# con.close()
	return 'OK'	
if __name__ == '__main__':
   app.run(debug = True, port = 8082)