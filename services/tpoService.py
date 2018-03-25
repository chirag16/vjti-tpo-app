# TPO invites companies to come to the parent college for recruitment.

from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

JSON_DB_PATH = '../database'
USER_DB_NAME = 'users.json'
INVITED_COMPANY_DB_NAME = 'invited.json'
SCHEDULE_DB_NAME = 'schedule.json'

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

def addToSchedule(companyDetails):
	global schedule
	schedule["companies"].append(companyDetails)
	with open(os.path.join(JSON_DB_PATH, SCHEDULE_DB_NAME), "w") as db:
		json.dump(schedule, db)

@app.route("/", methods = ['GET'])
def welcomeToTPO():
	return jsonify({"message" : "Welcome to TPO!"})

#AUTHENTICATION :
@app.route("/authenticateStudent", methods = ['POST'])
def authenticateStudent():
	found = False
	auth = False
	for student in students:
		if request.json["id"] == student["id"]:
			found = True
			if request.json["password"] == student["password"]:
				auth = True
	if found:
		if auth :
			return jsonify({"message" : "success"})
		else:
			return jsonify({"message" : "auth fail"})

	return jsonify({"message" : "not found"})

@app.route("/authenticateCompany", methods = ['POST'])
def authenticateCompany():
	found = False
	auth = False
	for company in companies:
		if request.json["id"] == company["id"]:
			found = True
			if request.json["password"] == company["password"]:
				auth = True
	if found:
		if auth :
			return jsonify({"message" : "success"})
		else:
			return jsonify({"message" : "auth fail"})

	return jsonify({"message" : "not found"})

@app.route("/inviteCompany", methods = ['POST'])
def inviteCompany():
	for invitedCompany in invited["companies"] :
		if request.form["id"] == invitedCompany["id"]:
			return "<h2>Company has already been invited!</h2>"
	addToInvited({u"employmentType": request.form["employment"], u"id": request.form["id"], u"name": request.form["name"]})
	return "<h2>Company Invite Listed!</h2>"

@app.route("/scheduleCompany", methods = ['POST'])
def scheduleCompany():
	for sched in schedule["companies"]:
		if request.form["id"] == sched["id"]:
			if request.form["round"] == sched["roundType"]:
				return "<h2>Company has already been scheduled!</h2>"

		if request.form["date"] == sched["date"]:
			if request.form["time"] == sched["time"]:
				return "<h2>Slot Already Booked!</h2>"

	addToSchedule({u"date": request.form["date"], u"roundType": request.form["round"], u"id": request.form["id"], u"name": request.form["name"], u"time": request.form["time"]})
	return "<h2>Company Selection Rounds Scheduled!</h2>"

if __name__ == "__main__":
	app.run(debug = True, port = 8081)