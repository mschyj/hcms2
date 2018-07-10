# encoding:UTF-8
import requests,os,ConfigParser,json,time
import re,commands
from elasticluster import log
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
class Session:
    def __init__(self):
        home = os.environ['HOME']
        self.config = ConfigParser.ConfigParser()
        self.path = home+"/.hwcc/config"
        self.config.read(self.path)
        sections = self.config.sections()
        cloud_section = None
        for section in sections:
            if  re.match(r'cloud',section) is not None:
                cloud_section = section
        username_encrypt = self.config.get(cloud_section,"username")
        self.username = self._decrypt( username_encrypt )
        password_encrypt = self.config.get(cloud_section,"password")
        self.password = self._decrypt( password_encrypt )
        self.domain_name = self.config.get(cloud_section,"user_domain_name")
        self.project_name = self.config.get(cloud_section,"project_name")
        self.auth_url = self.config.get(cloud_section,"auth_url")
        self.project_id	= None	    
	self.cbc_endpoint = "bss.%s.myhuaweicloud.com"%self.project_name	
	
	self.customer_id = "defd59fa033547c6a12948a614d93147"	    
    
    def _decrypt(self,text):
        cryptor = AES.new('1234567890123456',AES.MODE_CBC,b'0000000000000000')
        try:
	    plain_text = cryptor.decrypt(a2b_hex(text))
            return plain_text.rstrip('+')
        except TypeError,e:
            log.error("Your username/password seems not be encrypted:" + e.message)

    def auth(self):
        '''
        Auth function,send auth payload to keystone service
        '''
    
	auth_headers = {
            'Content-Type': 'application/json;charset=utf8',
        }
    
        auth_para = {"auth": {"identity": {"methods": ["password" ],
                               "password": {"user": {"name":self.username,"password":self.password,
                               "domain": {"name":self.domain_name }}} },
                               "scope": {"project": {"name": self.project_name}}}} 
        
	auth_para=json.dumps(auth_para)
	print "auth_para_sfs:%s"%auth_para
	print "auth_headers: %s"%auth_headers
	print "auth_url: %s"%self.auth_url
        try:
            auth_response = requests.post('%s/auth/tokens'%self.auth_url, headers=auth_headers, data=auth_para)
        except requests.ConnectionError as msg:
            raise ResponseError(str(msg))
    
        if auth_response.status_code != 201 and auth_response.status_code !=200:
            raise ResponseError("{0} status , msg:{1}".format(auth_response.status_code,auth_response.content))
    	try:
    	    token = auth_response.headers['X-Subject-Token']
            self.project_id =  auth_response.json()['token']['project']['id']
	    self.domain_id = auth_response.json()['token']['user']['domain']['id']
    	except:
    	    raise ResponseError("cannot find token in headers")
    	self.token = token
	print self.token

    def query_prePaidRes(self):
	'''      
	query prePaidRes
	
	'''
	query_res_headers = {
	'X-Auth-Token': self.token,
	     'Content-Type': 'application/json'
	 }
	self.order_id =  "CS1806251901EFVPT"
 
	try:
	    #url = 'https://%s/v1.0/%s/common/order-mgr/resources/detail?customer_id=%s&order_id=%s'%(self.cbc_endpoint,self.domain_id,self.domain_id,self.order_id)
	    url = 'https://%s/v1.0/%s/common/order-mgr/resources/detail?order_id=%s'%(self.cbc_endpoint,self.domain_id,self.order_id)  
	    #url = 'https://%s/v1.0/%s/common/order-mgr/resources/detail'%(self.cbc_endpoint,self.domain_id)
	    print url
	    #resinfo_response = requests.get(url, headers=query_res_headers)
	    resinfo_response = requests.get(url, headers=query_res_headers)
	except requests.ConnectionError	as msg:	    
	    raise ResponseError(str(msg))	
	if resinfo_response.status_code != 201 and resinfo_response.status_code !=200 :
	    raise ResponseError("{0} status , msg:{1}".format(resinfo_response.status_code,resinfo_response.content)) 
	resinfo_response = resinfo_response.json()
	total_count = resinfo_response['total_count']	
	self.flavor = "s2.small.1"
	
	if total_count == 0:
	    print "no resource "
	else:
	    data = resinfo_response['data']
	    for res_data in data:	
		if res_data['resource_type_code'] == 'hws.resource.type.vm':
		    print res_data['resource_id']
		
	
    
class ResponseError(Exception):
    pass	
if __name__ == "__main__":
    session = Session()
    session.auth()
    session.query_prePaidRes()  
