import xmlrpc.client

url = 'https://thymargo13-odoosh-dev-test1-1992912.dev.odoo.com'
db = 'thymargo13-odoosh-dev-test1-1992912'
username = 'admin'
password = 'admin'
model_session = 'academy.session'
model_course= 'academy.course'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())
#outpubt
#{'server_version': '14.0+e', 'server_version_info': [14, 0, 0, 'final', 0, 'e'], 'server_serie': '14.0', 'protocol_version': 1}

#Logging in
uid = common.authenticate(db,username,password, {})
print(uid)
#output: 2



models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# call methods of odoo models
# execute_kw(database, userid, password, model name, method name, list of param, dict of param)
model_access = models.execute_kw(db, uid, password, 
                                 model_session, 
                                 'check_access_rights',
                                 ['write'], 
                                 {'raise_exception':False})

#{'server_version': '14.0+e', 'server_version_info': [14, 0, 0, 'final', 0, 'e'], 'server_serie': '14.0', 'protocol_version': 1}
#2

courses = models.execute_kw(db, uid, password,model_course,
                           'search_read',
                            [[['level','in',['intermediate', 'beginner']]]])
print(courses)
# [{'id': 1, 'name': 'ERP 101', 'description': 'Learn ERP Systems', 'level': 'beginner', 'active': True, 'base_price': 0.0, 'additional_fee': 0.0, 'total_price': 0.0, 'session_ids': [], 'display_name': 'ERP 101', 'create_uid': [1, 'OdooBot'], 'create_date': '2021-01-26 07:17:27', 'write_uid': [1, 'OdooBot'], 'write_date': '2021-01-26 07:17:27', '__last_update': '2021-01-26 07:17:27'}]


course = models.execute_kw(db, uid, password,model_course,
                           'search',
                           [[['name','=','Accounting 200']]])
print(course) #[2] <==course.id

session_fields = models.execute_kw(db, uid, password,model_session, 'fields_get',
                                   [], {'attributes':['string', 'type', 'required']})
print(session_fields) 
# get fields

new_session = models.execute_kw(db, uid, password,model_session, 'create',
                                [
                                    {
                                        'course_id':course[0],
                                        'state':'open',
                                        'duration': 5,
                                    }
                                ]
                               )
print(new_session)

