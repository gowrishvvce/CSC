import MySQLdb
import json
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart


# CRUD for Survey

# tested works fine
def create_survey(survey_title,survey_category,user_id):
	cursor = db.cursor()
	sql = "INSERT INTO survey(survey_title,survey_category,user_id) VALUES('%s','%s','%d')"%(survey_title,survey_category,user_id)
	try:
  		cursor.execute(sql)
  		db.commit()
   	except Exception,e:
   		raise
		# print 'oops something went wrong' 
		# pass

	lastrowid = cursor.lastrowid
	cursor.close()

	return lastrowid


# tested
def get_surveys(user_id):
	cursor = db.cursor()
 	sql = "SELECT * FROM survey where user_id = '%d'"%(user_id)
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	surveys = []
 	for result in results:
 		survey_id = result[0]
 		survey_title  = result[1]
 		survey_category = result[2]
 		surveys.append({'survey_id':survey_id,'survey_title' : survey_title,'survey_category' : survey_category})
 	return surveys


def get_survey(sid):

	cursor = db.cursor()
	survey = {}
 	sql = "SELECT `survey`.id,`survey`.survey_title,`survey`.user_id,`survey_questions`.id,`survey_questions`.question,`survey_questions`.options FROM (`survey` INNER JOIN `survey_questions_mapping` on `survey`.id = '%d' and `survey`.id = `survey_questions_mapping`.sid INNER JOIN `survey_questions` on `survey_questions`.id = `survey_questions_mapping`.qid)"%(sid)
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	
 	survey['survey_title'] = results[0][1]
 	survey['survey_id'] = results[0][0]
 	survey['user_id'] = results[0][2]
 	questions = []

 	for result in results:
 		question = {}
 		question['qid'] = result[3]
 		question['question'] = result[4]
 		question['options'] = json.loads(result[5])
 		questions.append(question)
 	
 	survey['questions'] = questions

	return survey



# CRUD For questions

def create_question(question,options):

	cursor = db.cursor()
	sql = "INSERT INTO survey_questions(question,options) VALUES('%s','%s')"%(question,options)
	try:
  		cursor.execute(sql)
  		db.commit()
   	except Exception,e:
		raise

	lastrowid = cursor.lastrowid
	cursor.close()

	return lastrowid


#Mapping of survey and question
# tested
def insert_survey_questions_mapping(sid,qid):
	cursor = db.cursor()
	sql = "INSERT INTO survey_questions_mapping(sid,qid) VALUES('%d','%d')"%(sid,qid)
	try:
  		cursor.execute(sql)
  		db.commit()
   	except Exception,e:
		raise

	cursor.close()



# tested
def record_user_options(user_id,qid,optid):
	cursor = db.cursor()
	sql = "INSERT INTO user_answers(user_id,qid,optid) VALUES('%d','%d','%d')"%(user_id,qid,optid)
	try:
  		cursor.execute(sql)
  		db.commit()
   	except Exception,e:
		raise

	cursor.close()


# User management

# tested
def does_username_exist(user_name):
	cursor = db.cursor()
 	sql = "SELECT * FROM users where user_name = '%s'"%(thwart(user_name))
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	return len(results) > 0

# tested
def does_email_exist(user_email):
	cursor = db.cursor()
 	sql = "SELECT * FROM users where user_email = '%s'"%(thwart(user_email))
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	return len(results) > 0

# tested
def insert_user(user_name,first_name,last_name,user_email,user_password):
	
	cursor = db.cursor()
	user_password = sha256_crypt.encrypt(user_password)
	sql = "INSERT INTO users(user_name,first_name,last_name,user_email,user_password) VALUES('%s','%s','%s','%s','%s')"%(thwart(user_name),thwart(first_name),thwart(last_name),thwart(user_email),thwart(user_password))

	try:
  		cursor.execute(sql)
  		db.commit()
   	except Exception,e:
		raise

	lastrowid = cursor.lastrowid
	cursor.close()

	return lastrowid

# tested
def verify_login(user_name,user_password):

	cursor = db.cursor()
 	sql = "SELECT * FROM users where user_name = '%s'"%(thwart(user_name))
 	cursor.execute(sql)
 	results = cursor.fetchall()

	if(bool(results) and len(results) > 0):
 		if sha256_crypt.verify(user_password,results[0][5]):
 			return results[0][0]


 	return False




db = MySQLdb.connect(host = "localhost",user = "root",passwd = "root",db = "survey")

# get surveys
sid = 2
print get_survey(sid)
# User management tests
# Signup

# user_name = 'varunhegde93'
# first_name = 'varun'
# last_name = 'hegde'
# user_email = '1hvarun@gmail.com'
# user_password = 'varun123'

# user_id = insert_user(user_name,first_name,last_name,user_email,user_password)
# print 'The newly created user is '+str(user_id)


# Login 



# user_name = 'varunhegde93'
# user_email = '1hvarun@gmail.com'
# user_password = 'varun123'
# user_id =  verify_login(user_name,user_password)
# print int(user_id)
# print does_email_exist(user_email)
# print does_username_exist(user_name)
# User options
# record_user_options(1,3,1)

# Survey Questions Mapping
# insert_survey_questions_mapping(1,1)
# insert_survey_questions_mapping(1,2)
# insert_survey_questions_mapping(1,3)

# Survey question create
# question = "What is the name of your first pet"
# options = json.dumps(['Sony','Putti','Frodo'])
# qid = create_question(question,options)
# print "The created question is " + str(qid)

# Create a survey
# print get_surveys(1)
# uid = 1
# survey_title = "This is yet another test survey"
# survey_category = "Test"
# sid = create_survey(survey_title,survey_category,uid)
# print 'survey id is ' + str(sid)

# SELECT * FROM (`survey` INNER JOIN `survey_questions_mapping` on `survey`.id = 1 and `survey`.id = `survey_questions_mapping`.sid INNER JOIN `survey_questions` on `survey_questions`.id = `survey_questions_mapping`.qid)
