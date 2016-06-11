from flask import Flask, session, redirect, url_for, escape, request,render_template,url_for
import json
from db import *

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def not_found(error):
    return render_template('error.html'), 405


@app.route('/home',methods=['GET', 'POST'])
def home_route():
	# uid = request.args.get('uid')
	uid =  1
	surveys = get_surveys(uid)
	return render_template('home.html',surveys = surveys)

#dont worry now
@app.route('/login',methods=['GET','POST'])
def login():
	name = 'login'
	# username = request.form['username']
	print name
	return render_template('login.html',name = name)

# dont worry now
@app.route('/register',methods=['GET','POST'])
def register():
	name = 'register'
	print name
	return render_template('register.html',name = name)

@app.route('/admin',methods=['GET','POST'])
def admin():
	name = 'admin'
	print name
	return render_template('admin.html',name = name)

@app.route('/survey',methods=['GET','POST'])
def create_new_survey():
	
	if request.method == 'POST':
		# uid = int(str(request.form['uid']))
		uid = 1
		survey_title = str(request.form['survey_title'])
		survey_category = str(request.form['survey_category']) 
		sid = create_survey(survey_title,survey_category,uid)
		sid = str(sid)
		return redirect('/survey/'+sid)

	else:
		return render_template('create_survey.html')
		
		
# auth required
@app.route('/survey/<int:survey_id>',methods=['GET'])
def survey(survey_id):
	survey = get_survey(survey_id)
	return render_template('survey.html',survey = survey)


if __name__ == '__main__':
	app.run()

