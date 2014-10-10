import shutil
import os
import sys
import optparse
from java.util import HashSet
from java.io import FileOutputStream
from nmdeployment import NodeManagerDeployAPI
from esapi import EntityStoreAPI
#from com.vordel.api.deployment.model import DeploymentBundle
from com.vordel.api.deployment.model import DeploymentArchive
from com.vordel.es.fed.assembly import StoreManager
from com.vordel.es.fed.assembly import StoreType
from com.vordel.es.fed.assembly import Assembly
from com.vordel.api.deployment.client import DeploymentClient
from com.vordel.api.topology.client import TopologyClient

parser = optparse.OptionParser()
parser.add_option('--username', dest='username', type="string", help ="username to connect to apigateway admin nodemanager")
parser.add_option('--password', dest='password',type="string", help = "password to connect to apigateway admin nodemanager")
parser.add_option('--fed', dest='fed', type="string", help = "Fedfile name including entire path")
parser.add_option('--url', dest='url', type="string", help = "Url of apigateway admin nodemanager")
parser.add_option('--group', dest='group', type="string", help = "Group to which fed needs to be deployed")

(options, args) = parser.parse_args()

required = ['username', 'password', 'fed', 'url', 'group']
notpassed = []

for current in required:
    if not options.__dict__[current]:
        notpassed.append(current)
        print "option " + current  + " is missing"

if len(notpassed) > 0:
    parser.print_help()
    exit(-1)
        
print('username : ' + options.username)
print('password : ' + options.password)
print('fed file : ' + options.fed)
print('admin url : ' + options.url)
print('group : ' + options.group)

#fedToDeploy = DeploymentBundle(options.fed)
fedToDeploy = DeploymentArchive(options.fed)

#nmdep = NodeManagerDeployAPI(options.url, options.username, options.password)
print('-------------------------------------------------------------------')
print('Deploying to admin node manager at : ' + options.url)
#nmdep.deployToGroup(options.group, fedToDeploy)

deploymentClient = None
topologyClient = None

deploymentClient = DeploymentClient(options.url, options.username, options.password, 
                                None, None, bool(False))
topologyClient = TopologyClient(options.url, options.username, options.password, 
                                None, None, bool(False))   

group = topologyClient.getGroupByName(options.group)
deploymentClient.uploadConfigurationForDeployment(group.getId(), None, fedToDeploy)
# print("Deploying fed version/name : %s/%s" % (fedToDeploy.getVersion(), fedToDeploy.getName()))
print("Deploying fed")

for gateway in group.getServices():
     print("-------------------------------------------------------------------")
     print("Deploying fed to group/gateway : %s/%s" % (options.group, gateway.getName()))
         
     depResult = deploymentClient.deploy(gateway.getId(), fedToDeploy.getId())
     if(depResult.getStatus()):
        print ("Deployment Status : Success")
     else:
        print ("Deployment Status : Fail")
        print ("Failed due to %s" % (depResult.getFailureReason()))
        print ("Number of errors encountered during deployment %i" % (depResult.getErrorCount()))
        print("-------------------------------------------------------------------")
