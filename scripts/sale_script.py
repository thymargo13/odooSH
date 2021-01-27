import xmlrpc.client

url = 'https://thymargo13-odoosh-dev-test1-1992912.dev.odoo.com'
db = 'thymargo13-odoosh-dev-test1-1992912'
username = 'admin'
password = 'admin'

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
                                 'sale.order', 
                                 'check_access_rights',
                                 ['write'], 
                                 {'raise_exception':False})

print(model_access) #output: True


draft_quotes = models.execute_kw(db, uid, password, 
                                 'sale.order', 
                                 'search',
                                 [[['state','=','draft']]])
print(draft_quotes) #output :[3, 5, 2, 1] <-- id of order.


if_confirmed = models.execute_kw(db,uid, password,
                                'sale.order',
                                'action_confirm',
                                [draft_quotes])
print(if_confirmed)  #output: True