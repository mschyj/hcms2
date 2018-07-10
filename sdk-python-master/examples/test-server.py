import logging
import sys
import os
import time
print sys.path
sys.path.insert(0,'/root/sdk-python-master')
from openstack.connection import Connection        

from openstack import utils


utils.enable_logging(debug = True, stream = sys.stdout)

username = "yanjiao"
password = "Modify@0605"
projectId = "f8ae4f9fee254c4ea39b8998bbed6373"      
userDomainId = "fc17d84e262f4fb3b2b8bd3a990225f9"
projectName = "yanjiao"
userDomainName = "yanjiao"
auth_url = "https://iam.cn-north-1.myhwclouds.com/v3"



conn = Connection(
    auth_url=auth_url,
                             user_domain_id=userDomainId,
                             project_id=projectId,
                             username=username,
                             password=password,
                             verify=False
)
print "conn: %s"%conn

def test_compute():
    
    data = {
    "availability_zone": "cn-north-1a",
        "name": "test-period",
        "imageRef": "1189efbf-d48b-46ad-a823-94b942e2a000",
        "root_volume": {
            "volumetype": "SATA"
        },
        "isAutoRename": "true",
        "flavorRef": "s3.small.1",
        "security_groups": [
            {
                "id": "c5d250c2-1754-433d-8783-08d29b46822b"
            }
        ],
        "vpcid": "2abe252d-df1b-4060-8a9b-318b1c894856",
        "nics": [
            {
                "subnet_id": "328e440a-715c-48b9-a60a-f3b9d0fe1b85"
            }
        ],
        "key_name": "hwckey",
        "count": 1,
    "extendparam": {
            "chargingMode": "prePaid",
            "periodType": "month",
        "periodNum": 1,
            "isAutoRenew": "false",
        "isAutoPay": "true",
        "regionID": "cn-north-1"
    },
"metadata": {
        "op_svc_userid": "defd59fa033547c6a12948a614d93147"
    },        
    }               
    dds = conn.ecs.create_server_ext(**data) 
    print dds               

    print "====================%s"%dds.order_id

if __name__ == "__main__":      
        test_compute()  
