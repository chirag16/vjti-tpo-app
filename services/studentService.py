from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)

# WORKING_DIR_PATH	= '/home/chi/College Stuff/6th Sem/SADP Tutorials/microservices'
APPLICATIONS_PATH = '../database/applications.json'

@app.route('/student-application', methods = ['POST'])
def student_application():
	with open(APPLICATIONS_PATH, 'r') as f:
		applications = json.load(f)
	applications['entries'].append({ "name": request.form['name'], "company": request.form['company'], "status": "Undecided" })
	with open(APPLICATIONS_PATH, 'w') as f:
		json.dump(applications, f)
	return "<h2>Application Successful!</h2>"

@app.route('/student-application-status/<name>/<company>', methods = ['GET'])
def get_student_application_status(name, company):
	with open(APPLICATIONS_PATH, 'r') as f:
		applications = json.load(f)
	for application in applications['entries']:
		if application['name'] == name and application['company'] == company:
			student_name = application['name']
			company_name = application['company']
			application_status = application['status']
	return "Status:<br />\"name\": \"%s\",<br /> \"company\": \"%s\",<br /> \"status\": \"%s\"" % (student_name, company_name, application_status)

if __name__ == '__main__':
	app.run(port = 8000, debug = True)