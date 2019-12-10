import os
import sys
import requests
import time
import unittest
import json

import docker_control

dockerBuildTag = "testing" #put the tag for your docker build here

hostIp = "localhost" #localhost will not work here, it needs to be your machine's ip address, 
#on Docker Toolbox you will may need to run "docker-machine ip" to get the ip address you need.

needSudo = False # obviously if you need sudo, set this to True 
#contact me imediately if setting this to True breaks things 
#(I don't have a machine which needs sudo, so it has not been tested, although in theory it should be fine)

port_prefix = "8080"

propogationTime = 2 #sets number of seconds we sleep after certain actions to let data propagate through your system
# you may lower this to speed up your testing if you know that your system is fast enough to propigate information faster than this
# I do not recomend increasing this

dc = docker_control.docker_controller(needSudo)

def getViewString(view):
    listOStrings = []
    for instance in view:
        listOStrings.append(instance["testScriptAddress"])

    return listOStrings

# Basic Functionality
# These are the endpoints we should be able to hit
    #KVS Functions
def storeKeyValue(ipPort, key, value, payload):
    # print("ipPort: ", ipPort)
    #print('PUT: http://%s/keyValue-store/%s'%(str(ipPort), key))
    return requests.put( 'http://%s/keyValue-store/%s'%(str(ipPort), key), data={'val':value, 'payload': json.dumps(payload)} )

def checkKey(ipPort, key, payload):
    #print('GET: http://%s/keyValue-store/search/%s'%(str(ipPort), key))
    return requests.get( 'http://%s/keyValue-store/search/%s'%(str(ipPort), key), data={'payload': json.dumps(payload)} )

def getKeyValue(ipPort, key, payload):
    #print('GET: http://%s/keyValue-store/%s'%(str(ipPort), key))
    # return requests.get( 'http://%s/keyValue-store/%s'%(str(ipPort), key), data={'payload': json.dumps(payload)} )
    return requests.get( 'http://%s/keyValue-store/%s'%(str(ipPort), key))

def deleteKey(ipPort, key, payload):
    #print('DELETE: http://%s/keyValue-store/%s'%(str(ipPort), key))
    return requests.delete( 'http://%s/keyValue-store/%s'%(str(ipPort), key), data={'payload': json.dumps(payload)} )

    #Replication Functions
def addNode(ipPort, newAddress):
    #print('PUT: http://%s/view'%str(ipPort))
    return requests.put( 'http://%s/view'%str(ipPort), data={'ip_port':newAddress} )

def removeNode(ipPort, oldAddress):
    #print('DELETE: http://%s/view'%str(ipPort))
    return requests.delete( 'http://%s/view'%str(ipPort), data={'ip_port':oldAddress} )

def viewNetwork(ipPort):
    #print('GET: http://%s/view'%str(ipPort))
    return requests.get( 'http://%s/view'%str(ipPort) )

###########################################################################################

class TestHW3(unittest.TestCase):
    # view = {}
    view = ["0.0.0.0:8081","0.0.0.0:8082","0.0.0.0:8083"]

    # def setUp(self):
    #     print("Setup started...")
    #     self.view = dc.spinUpManyContainers(dockerBuildTag, hostIp, port_prefix, 2)

    # def tearDown(self):
    #     print("Cleanup started...")
    #     dc.cleanUpDockerContainer()


    def getPayload(self, ipPort, key):
        response = checkKey(ipPort, key, {})
        #print(response)
        data = response.json()
        return data["payload"]

    def confirmAddKey(self, ipPort, key, value, expectedStatus, expectedMsg, expectedReplaced, payload={}):
        response = storeKeyValue(ipPort, key, value, payload)

        # print(response)

        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['msg'], expectedMsg)
        self.assertEqual(data['replaced'], expectedReplaced)

        return data["payload"]


    def confirmCheckKey(self, ipPort, key, expectedStatus, expectedResult, expectedIsExists, payload={}):
        response = checkKey(ipPort, key, payload)
        #print(response)
        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['result'], expectedResult)
        self.assertEqual(data['isExists'], expectedIsExists)

        return data["payload"]


    def confirmGetKey(self, ipPort, key, expectedStatus, expectedResult, expectedValue=None, expectedMsg=None, payload={}):
        response = getKeyValue(ipPort, key, payload)
        #print(response)
        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        # print("data: ", data)
        self.assertEqual(data['result'], expectedResult)
        if expectedValue != None and 'value' in data:
            # print("data: ", data)
            self.assertEqual(data['value'], expectedValue)
        if expectedMsg != None and 'msg' in data:
            self.assertEqual(data['msg'], expectedMsg)

        return data["payload"]


    def confirmDeleteKey(self, ipPort, key, expectedStatus, expectedResult, expectedMsg, payload={}):
        response = deleteKey(ipPort, key, payload)
        #print(response)

        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['result'], expectedResult)
        self.assertEqual(data['msg'], expectedMsg)

        return data["payload"]

    def confirmViewNetwork(self, ipPort, expectedStatus, expectedView):
        response = viewNetwork(ipPort)
        #print(response)
        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()

        print(data['view'])

        print(expectedView)

        self.assertEqual(data['view'], expectedView)

    def confirmAddNode(self, ipPort, newAddress, expectedStatus, expectedResult, expectedMsg):
        response = addNode(ipPort, newAddress)

        #print(response)

        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['result'], expectedResult)
        self.assertEqual(data['msg'], expectedMsg)

    def confirmDeleteNode(self, ipPort, removedAddress, expectedStatus, expectedResult, expectedMsg):
        response = removeNode(ipPort, removedAddress)
        #print(response)
        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['result'], expectedResult)
        self.assertEqual(data['msg'], expectedMsg)


##########################################################################################################

# Confirm Basic functionality:

    def test_a_add_key_value_one_node(self):
        
        ipPort = self.view[0]
        key = "addNewKey"
        
        payload = self.getPayload(ipPort, key)
        
        payload = self.confirmAddKey(ipPort=ipPort, 
                           key=key, 
                           value="a simple value", 
                           expectedStatus=200, 
                           expectedMsg="Added successfully", 
                           expectedReplaced=False,
                           payload= payload)
        
        value = "aNewValue"

        payload = self.confirmAddKey(ipPort=ipPort, 
                           key=key, 
                           value=value, 
                           expectedStatus=201, 
                           expectedMsg="Updated successfully", 
                           expectedReplaced=True,
                           payload=payload)

        payload = self.confirmCheckKey(ipPort=ipPort, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=True,
                           payload=payload)

        payload = self.confirmGetKey(ipPort=ipPort, 
                           key=key, 
                           expectedStatus=200, 
                           expectedResult="Success", 
                           expectedValue=value,
                           payload=payload)

    def test_b_add_key_value_two_nodes(self):
        
        ipPortOne = self.view[0]
        ipPortTwo = self.view[1]
        key = "keyOnBothNodes"
        value = "aValue"

        payload = self.getPayload(ipPortOne, key)

        payload = self.confirmAddKey(ipPort=ipPortOne, 
                           key=key, 
                           value=value, 
                           expectedStatus=200, 
                           expectedMsg="Added successfully", 
                           expectedReplaced=False,
                           payload=payload)

        payload = self.confirmCheckKey(ipPort=ipPortOne, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=True,
                            payload=payload)

        time.sleep(propogationTime)

        payload = self.confirmCheckKey(ipPort=ipPortTwo, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=True,
                            payload=payload)

        payload = self.confirmGetKey(ipPort=ipPortTwo, 
                           key=key, 
                           expectedStatus=200, 
                           expectedResult="Success", 
                           expectedValue=value,
                           payload=payload)

    def test_c_delete_value_one_node(self):
        
        ipPort = self.view[0]
        key = "keyToBeDeletedFromOneNode"
        value = "aValue"

        payload = self.getPayload(ipPort, key)

        payload = self.confirmAddKey(ipPort=ipPort, 
                           key=key, 
                           value=value, 
                           expectedStatus=200, 
                           expectedMsg="Added successfully", 
                           expectedReplaced=False,
                           payload=payload)

        payload = self.confirmCheckKey(ipPort=ipPort, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=True,
                            payload=payload)

        payload = self.confirmDeleteKey(ipPort=ipPort, 
                              key=key, 
                              expectedStatus=200, 
                              expectedResult="Success", 
                              expectedMsg="Key deleted",
                              payload=payload)

        payload = self.confirmCheckKey(ipPort=ipPort, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=False,
                            payload=payload)

    def test_d_delete_value_two_nodes(self):
        
        ipPortOne = self.view[0]
        ipPortTwo = self.view[1]
        key = "keyToBeDeletedFromTwoNodes"
        value = "aValue"

        payload = self.getPayload(ipPortOne, key)
        #add the key
        payload = self.confirmAddKey(ipPort=ipPortTwo, 
                           key=key, 
                           value=value, 
                           expectedStatus=200, 
                           expectedMsg="Added successfully", 
                           expectedReplaced=False,
                           payload=payload)

        payload = self.confirmCheckKey(ipPort=ipPortTwo, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=True,
                            payload=payload)

        time.sleep(propogationTime)

        payload = self.confirmCheckKey(ipPort=ipPortOne, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=True,
                            payload=payload)


        #delete the key
        payload = self.confirmDeleteKey(ipPort=ipPortOne, 
                              key=key, 
                              expectedStatus=200, 
                              expectedResult="Success", 
                              expectedMsg="Key deleted",
                              payload=payload)

        payload = self.confirmCheckKey(ipPort=ipPortOne, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=False,
                            payload=payload)

        time.sleep(propogationTime)

        payload = self.confirmCheckKey(ipPort=ipPortTwo, 
                            key=key, 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=False,
                            payload=payload)

    def test_e_check_nonexistantKey(self):
        
        self.confirmCheckKey(ipPort=self.view[0],
                            key="SomethingWhichDoesNotExist", 
                            expectedStatus=200, 
                            expectedResult="Success", 
                            expectedIsExists=False)

    def test_f_get_nonexistantKey(self):
        
        self.confirmGetKey(ipPort=self.view[0],
                           key="SomethingWhichDoesNotExist",
                           expectedStatus=404, 
                           expectedResult="Error", 
                           expectedMsg="Key does not exist")

    def test_g_delete_nonexistantKey(self):
        
        self.confirmDeleteKey(ipPort=self.view[0],
                              key="SomethingWhichDoesNotExist", 
                              expectedStatus=404, 
                              expectedResult="Error", 
                              expectedMsg="Key does not exist")

# #   Everything up to this point could be done via message forwarding, as in assignment 2
# #   However, if that is all you are doing, the following tests should fail

    def test_h_get_view(self):
        viewSting = getViewString(self.view)

        self.confirmViewNetwork(ipPort=self.view[0],
                        expectedStatus=200, 
                        expectedView=viewSting)

#     def test_i_add_node_to_network(self):
#         ipPort = self.view[0]["testScriptAddress"]

#         newPort = "%s4"%port_prefix
#         newView = "%s:%s"%(hostIp, newPort)

#         viewSting = getViewString(self.view)
#         viewSting.append(newView)

#         newNode = dc.spinUpDockerContainer(dockerBuildTag, hostIp, newPort, ",".join(viewSting))

#         self.view.append(newNode)

#         self.confirmAddNode(ipPort=ipPort, 
#                             newAddress=newView, 
#                             expectedStatus=200, 
#                             expectedResult="Success", 
#                             expectedMsg="Successfully added %s to view"%newView)

#         for node in self.view:
#             self.confirmViewNetwork(ipPort=node["testScriptAddress"], 
#                                     expectedStatus=200, 
#                                     expectedView=viewSting)


#     def test_j_remove_node_from_network(self):
#         ipPort = self.view[0]["testScriptAddress"]
#         removedNode = self.view.pop()

#         self.confirmDeleteNode(ipPort=ipPort, 
#                                removedAddress=removedNode["testScriptAddress"], 
#                                expectedStatus=200, 
#                                expectedResult="Success", 
#                                expectedMsg="Successfully removed %s from view"%removedNode["testScriptAddress"])

#         for node in self.view:
#             self.confirmViewNetwork(ipPort=node["testScriptAddress"], 
#                                     expectedStatus=200, 
#                                     expectedView=getViewString(self.view))

#     def test_k_replication_add_node_get_up_to_speed(self):
#         key = "OhLookAKey"
#         value = "AndHeyAValue"
#         ipPort = self.view[0]["testScriptAddress"]

#         payload = self.getPayload(ipPort, key)

#         payload = self.confirmAddKey(ipPort=ipPort, 
#                             key=key, 
#                             value=value, 
#                             expectedStatus=200, 
#                             expectedMsg="Added successfully", 
#                             expectedReplaced=False,
#                             payload=payload)

#         self.test_i_add_node_to_network()

#         time.sleep(propogationTime)

#         newIpPort = self.view[2]["testScriptAddress"]

#         payload = self.confirmCheckKey(ipPort=newIpPort, 
#                             key=key, 
#                             expectedStatus=200, 
#                             expectedResult="Success", 
#                             expectedIsExists=True,
#                             payload=payload)

#         payload = self.confirmGetKey(ipPort=self.newIpPort, 
#                            key=key, 
#                            expectedStatus=200, 
#                            expectedResult="Success", 
#                            expectedValue=value,
#                            payload=payload)

#     def test_l_replication_add_node_keep_up_to_speed(self):
#         key = "HeyIGotANewKey"
#         value = "YouShouldKnowAboutItToo"

#         ipPort=self.view[0]["testScriptAddress"]

#         self.test_i_add_node_to_network()

#         payload = self.getPayload(ipPort, key)

#         payload = self.confirmAddKey(ipPort=self.view[0]["testScriptAddress"], 
#                             key=key, 
#                             value=value, 
#                             expectedStatus=200, 
#                             expectedMsg="Added successfully", 
#                            expectedReplaced=False,
#                            payload=payload)

#         time.sleep(propogationTime)

#         newIpPort = self.view[2]["testScriptAddress"]

#         payload = self.confirmCheckKey(ipPort=newIpPort, 
#                             key=key, 
#                             expectedStatus=200, 
#                             expectedResult="Success", 
#                             expectedIsExists=True,
#                             payload=payload)

#         payload =self.confirmGetKey(ipPort=newIpPort, 
#                            key=key, 
#                            expectedStatus=200, 
#                            expectedResult="Success", 
#                            expectedValue=value,
#                            payload=payload)

#     def test_m_replication_add_node_make_sure_it_tells_everyone_else_about_new_things(self):
#         key = "HeyIGotANewKey"
#         value = "YouShouldKnowAboutItToo"

#         self.test_i_add_node_to_network()

#         ipPort = self.view[1]["testScriptAddress"]
#         newIpPort = self.view[2]["testScriptAddress"]

#         payload = self.getPayload(ipPort, key)

#         payload = self.confirmAddKey(ipPort=newIpPort, 
#                                     key=key, 
#                                     value=value, 
#                                     expectedStatus=200, 
#                                     expectedMsg="Added successfully", 
#                                     expectedReplaced=False,
#                                     payload=payload)

#         time.sleep(propogationTime)

#         payload = self.confirmCheckKey(ipPort=ipPort, 
#                             key=key, 
#                             expectedStatus=200, 
#                             expectedResult="Success", 
#                             expectedIsExists=True,
#                            payload=payload)

#         payload = self.confirmGetKey(ipPort=ipPort, 
#                            key=key, 
#                            expectedStatus=200, 
#                            expectedResult="Success", 
#                            expectedValue=value,
#                            payload=payload)

#     def test_n_replication_remove_node(self):
#         key = "HeyWhereDidYouGo"
#         value = "IllHoldYourStuffWhileYoureGone"

#         stationaryNode = self.view[0]["testScriptAddress"]
#         removedNode = self.view.pop()

#         payload = self.getPayload(removedNode["testScriptAddress"], key)

#         payload = self.confirmAddKey(ipPort=removedNode["testScriptAddress"], 
#                             key=key, 
#                             value=value, 
#                             expectedStatus=200, 
#                             expectedMsg="Added successfully", 
#                             expectedReplaced=False,
#                             payload=payload)

#         self.confirmDeleteNode(ipPort=stationaryNode, 
#                                removedAddress=removedNode["testScriptAddress"], 
#                                expectedStatus=200, 
#                                expectedResult="Success", 
#                                expectedMsg="Successfully removed %s from view"%removedNode["testScriptAddress"])

#         payload = self.confirmCheckKey(ipPort=stationaryNode, 
#                                         key=key, 
#                                         expectedStatus=200, 
#                                         expectedResult="Success", 
#                                         expectedIsExists=True,
#                                         payload=payload)

#         payload = self.confirmGetKey(ipPort=stationaryNode, 
#                                        key=key, 
#                                        expectedStatus=200, 
#                                        expectedResult="Success", 
#                                        expectedValue=value,
#                                        payload=payload)

#     def test_o_replication_remove_node_dont_talk_to_the_dead(self):
#         key = "TheDeadCannotHear"
#         value = "SoWeCanSayTheySmellAndTheydNeverKnow"

#         stationaryNode = self.view[0]["testScriptAddress"]
#         removedNode = self.view.pop()

#         self.confirmDeleteNode(ipPort=stationaryNode, 
#                                removedAddress=removedNode["testScriptAddress"], 
#                                expectedStatus=200, 
#                                expectedResult="Success", 
#                                expectedMsg="Successfully removed %s from view"%removedNode["testScriptAddress"])

#         payload = self.getPayload(stationaryNode, key)

#         payload = self.confirmAddKey(ipPort=stationaryNode, 
#                             key=key, 
#                             value=value, 
#                             expectedStatus=200, 
#                             expectedMsg="Added successfully", 
#                             expectedReplaced=False,
#                             payload=payload)

#         time.sleep(propogationTime)

#         payload = self.confirmCheckKey(ipPort=removedNode["testScriptAddress"], 
#                             key=key, 
#                             expectedStatus=200, 
#                             expectedResult="Success", 
#                             expectedIsExists=False,
#                             payload=payload)

#     def test_p_replication_sudden_failure(self):
#         key = "ThisLand"
#         value = "CurseYourSuddenButInevitableBetrayal"

#         failedNode = self.view[0]
#         liveNode = self.view[1]["testScriptAddress"]

#         payload = self.getPayload(liveNode, key)

#         payload = self.confirmAddKey(ipPort=failedNode["testScriptAddress"], 
#                             key=key, 
#                             value=value, 
#                             expectedStatus=200, 
#                             expectedMsg="Added successfully", 
#                             expectedReplaced=False,
#                             payload=payload)

#         time.sleep(propogationTime)

#         dc.cleanUpDockerContainer(failedNode["containerID"])

#         payload = self.confirmCheckKey(ipPort=liveNode, 
#                             key=key, 
#                             expectedStatus=200, 
#                             expectedResult="Success", 
#                             expectedIsExists=True,
#                             payload=payload)

#         payload = self.confirmGetKey(ipPort=liveNode, 
#                            key=key, 
#                            expectedStatus=200, 
#                            expectedResult="Success", 
#                            expectedValue=value,
#                            payload=payload)
    
# Is Causually Consistent

#    def test_causual_consistency(self):

if __name__ == '__main__':

    unittest.main() 