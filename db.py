import MySQLdb
import json


# CRUD for Survey

# tested works fine
def create_survey(survey_title,survey_category,uid):
	cursor = db.cursor()
	sql = "INSERT INTO survey(survey_title,survey_category,uid) VALUES('%s','%s','%d')"%(survey_title,survey_category,uid)
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
def get_surveys(uid):
	cursor = db.cursor()
 	sql = "SELECT * FROM survey where uid = '%d'"%(uid)
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	surveys = []
 	for result in results:
 		survey_id = result[0]
 		survey_title  = result[1]
 		survey_category = result[2]
 		surveys.append({'survey_id':survey_id,'survey_title' : survey_title,'survey_category' : survey_category})
 	return surveys

# yet to be tested
def get_survey(sid):
	cursor = db.cursor()
 	sql = "SELECT * FROM survey where id ='%d'"%(sid)#join statement
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	if bool(results):
	 	return results[0]

	return None



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


def get_question(sid,qid):
	cursor = db.cursor()
 	sql = "SELECT * FROM surveys where sid = '%d'"%(sid)#join statement
 	cursor.execute(sql)
 	results = cursor.fetchall()
 	return results
	




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
def record_user_options(uid,qid,optid):
	cursor = db.cursor()
	sql = "INSERT INTO user_answers(uid,qid,optid) VALUES('%d','%d','%d')"%(uid,qid,optid)
	try:
  		cursor.execute(sql)
  		db.commit()
   	except Exception,e:
		raise

	cursor.close()






db = MySQLdb.connect(host = "localhost",user = "root",passwd = "root",db = "survey")

# User options
# record_user_options(1,3,1)

# Survey Questions Mapping
# insert_survey_questions_mapping(1,1)
# insert_survey_questions_mapping(1,2)
# insert_survey_questions_mapping(1,3)

# Survey question create
# question = "What is the name of your first pet"
# options = json.dumps(["Sony","Putti","Frodo"])
# qid = create_question(question,options)
# print "The created question is " + str(qid)

# Create a survey
# print get_surveys(1)
# uid = 1
# survey_title = "This is yet another test survey"
# survey_category = "Test"
# sid = create_survey(survey_title,survey_category,uid)
# print 'survey id is ' + str(sid)
