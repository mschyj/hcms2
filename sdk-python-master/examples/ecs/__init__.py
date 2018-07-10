#! /usr/bin/env python
# -*- coding:utf-8 -*-

def main():
    import os,sys
    sys.path.insert(0,'/root/sdk-python-master')   
    print sys.path
    from openstack import connection
    from  auth import Auth
     
    from server import create_server_ext
    conn = Auth().getConnection()

    create_server_ext(conn)


    
pass


if __name__ == '__main__':
    main()