#!/usr/bin/env python

import getpass
import sys
import os
import ConfigParser

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client as nova_client
from neutronclient.v2_0 import client as neutron_client
from neutronclient.common.exceptions import BadRequest as BadNeutronRequest

from encrypt import AESCrypto

home=os.environ['HOME']
config=ConfigParser.ConfigParser()
config.read(home + "/.hwcc/config")
username=config.get("cloud/hwc","username")
password=config.get("cloud/hwc","password")
pc=AESCrypto()
username=pc.decrypt(username)
password=pc.decrypt(password)
auth_url=config.get("cloud/hwc","auth_url")
user_domain_name=config.get("cloud/hwc","user_domain_name")
project_domain_name=config.get("cloud/hwc","project_domain_name")
project_name=config.get("cloud/hwc","project_name")

local_user=getpass.getuser()
remote_user=config.get("login/linux","image_user")
ssh_files=[home+"/.ssh/id_rsa",home+"/.ssh/id_rsa.pub",home + "/.ssh/authorized_keys"]

auth = v3.Password(
       username=username,
       password=password,
       auth_url=auth_url,
       user_domain_name=user_domain_name,
       project_domain_name=project_domain_name,
       project_name=project_name
    )
		
def start_vm(vmname):
  found=False
  sess = session.Session(auth=auth, verify=True)
  #print sess.get_endpoint(service_type='compute',interface='public')
  novacli = nova_client.Client("2.1", session=sess)
  instances=novacli.servers.list()
  #print instances
  if vmname == 'all':
    for vm in instances:
      if vm.status == 'SHUTOFF':
        print vm.name + " is starting"
        print vm.status
        novacli.servers.start(vm)
        found = True
  else:
    for vm in instances:
      if vm.name == vmname:
        print vm.name + " is starting"
        novacli.servers.start(vm)
        found = True
  if(not found):
    print vmname + " is not found"

def stop_vm(vmname):
  found=False
  sess = session.Session(auth=auth, verify=True)
  #print sess.get_endpoint(service_type='compute',interface='public')
  novacli = nova_client.Client("2.1", session=sess)
  instances=novacli.servers.list()
  #print instances
  for vm in instances:
    if vm.name == vmname:
      print vm.name + " is stopping"
      novacli.servers.stop(vm)
      found = True
  if(not found):
    print vmname + " is not found"
	
def get_vm_ip(vmname):
  found=False
  frontip=0
  sess = session.Session(auth=auth, verify=True)
  novacli = nova_client.Client("2.1", session=sess)
  instances=novacli.servers.list()
  for vm in instances:
    if vm.name == vmname:
      IPs = sum(vm.networks.values(),[])
      frontip=IPs[0]
      found = True
  if(not found):
    print vmname + " is not found"
  return frontip

def find_vm(vmname):
  sess = session.Session(auth=auth, verify=True)
  novacli = nova_client.Client("2.1", session=sess)
  try:
    vm = novacli.servers.find(name=vmname)
    print vm
  except AttributeError:
    print "Attribute Error"
  except nova_client.exceptions.NotFound:
    print "Not Found"

def get_vpc_id(subnet_id):
  sess = session.Session(auth=auth, verify=True)
  neutroncli = neutron_client.Client(session=sess)
  networks = neutroncli.list_networks(retrieve_all=True)['networks']
  for network in networks:
    if subnet_id == network['id']:
      vpc_id = network['name']
  return vpc_id

def get_all_nodes(template,cluster_name):
  sess = session.Session(auth=auth, verify=True)
  novacli = nova_client.Client("2.1", session=sess)
  vms=novacli.servers.list()
  subnet_id = config.get("cluster/"+template,"network_ids")
  vpc_id = get_vpc_id(subnet_id)
  nodes = []
  for vm in vms:
    vpcid = vm.networks.keys()
    if vpcid[0] == vpc_id and vm.name.startswith(cluster_name+"-"):
       ips = sum(vm.networks.values(),[])
       priv_ip = ips[0]
       node = {}
       node['kind'] = "worker"
       node['instance_id'] = vm.id
       node['private_ip'] = priv_ip
       nodes.append(node)
  find = False
  while True:
    master_node_id = raw_input("Specify your instance id of master node: ")
    for node in nodes:
      if master_node_id == node['instance_id']:
        nodes.remove(node)
        node['kind'] = "master"
        nodes.insert(0,node)
        find = True
        break
    if find:
      break 
    else:
      print("No valid instance id is found, please input a valid instance.")
  return nodes

def init_ssh():
  print "init ssh"

if __name__ == "__main__":
  print ('This is main of module "vm.py"')
  #get_vpc_id("c4c0301b-954f-4fbf-85d2-0ff370b51c00")
  get_all_nodes("c4c0301b-954f-4fbf-85d2-0ff370b51c00","slurm")
  #get_vm_ip("slurm-master001")
  #start_vm('all')
  #find_vm("slurm-frontend004")
