from flask import Flask, session, redirect, url_for, escape, request,render_template,url_for,jsonify
import json
from db import *
from functools import wraps

app = Flask(__name__)
app.secret_key = "enter your secret key here"
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_TYPE'] = 'memcached'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
        	return f(*args, **kwargs)
        
        return redirect(url_for('login'))
	return wrap


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
	user_name = ''
	if 'user_name' in session:
		user_name = session['user_name']

	return render_template('home.html',surveys = surveys,username = user_name)

# works
@app.route('/login',methods=['GET','POST'])
def login():
	
	error = None
	message = {'success' : 0,'message' : ''}
	
	if request.method == 'POST':

		user_name = str(request.form['user_name'])
		user_password = str(request.form['user_password'])

		if verify_login(user_name,user_password):
			session['logged_in'] = True
			session['user_name'] = user_name
			message = {'success' : 1,'message':'User Successfully logged in'}
 		else:
			error = 'Invalid username or password'
			message = {'success' : 0,'message' : error}
		
		return jsonify(results=message)
			

	return render_template('login.html')

# works
@app.route('/register',methods=['GET','POST'])
def register():
	
	errors = []
	message = {'success' : 0,'message' : ''}

	if request.method == 'POST':

		user_name = str(request.form['user_name'])
		first_name = str(request.form['first_name']) 
		last_name = str(request.form['last_name'])
		user_password = str(request.form['user_password'])
		user_email = str(request.form['user_email'])

		if does_username_exist(user_name):
			errors.append("User name already exists")

		if does_email_exist(user_email):
			errors.append("User email already exists")

		if bool(errors):
			message = {'success' : 0,'message' : errors}
		else:
			try:
				user_id = insert_user(user_name,first_name,last_name,user_email,user_password)
				session['logged_in'] = True
				session['user_name'] = user_name
				message = {'success' : 1,'message' : 'Successfully registered'}

			except Exception, e:
				raise
				errors = []
				errors.append("Something went wrong please try again")
				message = {'success' : 0,'message' : errors}
			
		return jsonify(results=message)


	return render_template('register.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
	name = 'admin'
	print name
	return render_template('admin.html',name = name)


@app.route('/save_options',methods=['POST'])
def save_options():
	
	question = str(request.form['question'])
	options = str(request.form['options'])

	try:
		question_id = create_question(question,options)
		# if isinstance(question_id, int ):
		message = {'success':1,'message' : 'Successfully created'}
			
	except Exception, e:
		message = {'success':0,'message' : 'Something went wrong'}
	
	return jsonify(results=message)
	


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

