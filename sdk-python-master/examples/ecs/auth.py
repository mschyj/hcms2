import os,sys
sys.path.insert(0,'/root/sdk-python-master')
from openstack import connection
class Auth(object):


        def __init__(self):
                username = "yanjiao"
                password = "Modify@0605"
                region = "cn-north-1a"
                project_name = "yanjiao"
                user_domain_name = "yanjiao" 
                auth_url = "https://iam.cn-north-1.myhwclouds.com/v3" 
                print password
                auth_args ={        
                'auth_url': auth_url,
                'project_name': project_name,
                'username': username,
                'password': password,
                "region": region,
                "user_domain_name":user_domain_name
            # "cert":"e:\cert\xenca.crt",
                 }
            # verify false will ignore ssl verify
                self.conn = connection.Connection(verify=False, **auth_args)  
            #otc_env='otc-xen'
            #config = ConfigParser.ConfigParser()
            #config.readfp(open('C:\cloud.ini'))
            #username = config.get(otc_env,'username')
            #pasword = config.get(otc_env,'password')
            #project_name = config.get(otc_env,'project_name')
            #region = config.get(otc_env,'region')
            #user_domain_name=config.get(otc_env,'user_domain_name')
            #auth_url=config.get(otc_env,'auth_url')


           
                          

#         print auth_url
#         print username
#         print password
#         print project_name
#         print region
#         print user_domain_name

        def getConnection(self):
                return self.conn
            

        def getProperty(self, key):
                otc_env='otc-xen'
                config = ConfigParser.ConfigParser()
                config.readfp(open('C:\cloud.ini'))
                return config.get(otc_env, key)                
                 

        # get external network
        def get_external_network(self):
                for network_each in self.conn.network.networks():
                        if network_each.is_router_external == True :
                                return network_each                
           

if __name__ == '__main__':
        
#     for o in  Auth().getConnection().compute.keypairs():
#         print o.name
        print Auth().getProperty('username')
