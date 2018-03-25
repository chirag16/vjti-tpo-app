from flask import *
import sqlite3 as sql
app = Flask(__name__)

@app.route('/studentApplies')
def new_request():
	return render_template('studentApplies1.html')

@app.route('/insert', methods = ['POST', 'GET'])
def insert():
	if request.method == 'POST':
		try:
			id = request.form['id']
			student_name = request.form['student_name']
			branch = request.form['branch']
			pointer = request.form['pointer']
			
			
			con = sql.connect(r"C:\Users\Nidhi\Desktop\Ankit\SADP\Microservice\StudentDb.db") 
			cur = con.cursor()
			cur.execute("INSERT INTO students(id, name, branch, pointer) VALUES( ?, ?, ?, ?)", (id, student_name, branch, pointer) )
			con.commit()
			msg = "Record inserted"
		except Exception as e:
			con.rollback()
		
			msg = "Error in insertion"
		finally:
			return render_template('resultStudentApplies.html', msg = msg)
			con.close()
	return 'OK'

			
			
if __name__ == '__main__':
   app.run(debug = True)