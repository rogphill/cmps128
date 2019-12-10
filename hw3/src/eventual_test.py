"""
    Credit:
        https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format  
"""
# last update:  11/17/18 - changed to use subnets, since Mac and Linux apparently really need them
# past updates: 11/10/18 - fixed the expected result of GET view


import os
import sys
import requests
import time
import unittest
import json
import asyncio
from aiohttp import ClientSession

import docker_control

dockerBuildTag = "testing" #put the tag for your docker build here

hostIp = "localhost" # this can be localhost again

needSudo = False # obviously if you need sudo, set this to True 
#contact me imediately if setting this to True breaks things 
#(I don't have a machine which needs sudo, so it has not been tested, although in theory it should be fine)

port_prefix = "808" #should be the first part of 8080 and the like, there should be no reason to change this
opt = "nil"
networkName = "mynet" # the name of the network you created

# networkIpPrefix = "192.168.0." # should be everything up to the last period of the subnet you specified when you 
networkIpPrefix = "10.0.0."
# created your network

propogationTime = 3 #sets number of seconds we sleep after certain actions to let data propagate through your system
# you may lower this to speed up your testing if you know that your system is fast enough to propigate information faster than this
# I do not recomend increasing this

dc = docker_control.docker_controller(networkName, needSudo)

def getViewString(view):
    listOStrings = []
    for instance in view:
        listOStrings.append(instance["networkIpPortAddress"])

    return ",".join(listOStrings)

def viewMatch(collectedView, expectedView):
    collectedView = collectedView.split(",")
    expectedView = expectedView.split(",")

    if len(collectedView) != len(expectedView):
        return False

    for ipPort in expectedView:
        if ipPort in collectedView:
            collectedView.remove(ipPort)
        else:
            return False

    if len(collectedView) > 0:
        return False
    else:
        return True


# Basic Functionality
# These are the endpoints we should be able to hit
    #KVS Functions
def storeKeyValue(ipPort, key, value, payload):
    #print('PUT: http://%s/keyValue-store/%s'%(str(ipPort), key))
    return requests.put( 'http://%s/keyValue-store/%s'%(str(ipPort), key), data={'val':value, 'payload': json.dumps(payload)} )

def checkKey(ipPort, key, payload):
    #print('GET: http://%s/keyValue-store/search/%s'%(str(ipPort), key))
    return requests.get( 'http://%s/keyValue-store/search/%s'%(str(ipPort), key), data={'payload': json.dumps(payload)} )

def getKeyValue(ipPort, key, payload):
    #print('GET: http://%s/keyValue-store/%s'%(str(ipPort), key))
    return requests.get( 'http://%s/keyValue-store/%s'%(str(ipPort), key), data={'payload': json.dumps(payload)} )

def deleteKey(ipPort, key, payload):
    #print('DELETE: http://%s/keyValue-store/%s'%(str(ipPort), key))
    return requests.delete( 'http://%s/keyValue-store/%s'%(str(ipPort), key), data={'payload': json.dumps(payload)} )

    #Replication Functions
def addNode(ipPort, newAddress):
    #print('PUT: http://%s/view'%str(ipPort))
    return requests.put( 'http://%s/view'%str(ipPort), data={'ip_port':newAddress} )

def removeNode(ipPort, oldAddress):
    #print('DELETE: http://%s/view'%str(ipPort))
    url = 'http://%s/view'%str(ipPort)
    print("Url: ", url)
    print("oldAddress: ", oldAddress)
    return requests.delete( url, data={'ip_port':oldAddress} )

def viewNetwork(ipPort):
    #print('GET: http://%s/view'%str(ipPort))
    return requests.get( 'http://%s/view'%str(ipPort) )

async def fetch(url, session):
    async with session.put('http://%s/keyValue-store/%s'%(str(url[0]), url[1]), data={'val':url[2], 'payload': json.dumps(url[3])}) as response:
        return await response.read()

async def run(urlList):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for url in urlList:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses
        # you now have all response bodies in this variable



###########################################################################################

class TestHW3(unittest.TestCase):
    view = {}

    @classmethod
    def setUpClass(cls):
        """ get_some_resource() is slow, to avoid calling it for each test use setUpClass()
            and store the result as class variable
        """
        super(TestHW3, cls).setUpClass()
        opt = cls.BUILD
        dc.buildDockerImage("testing", opt)

    def setUp(self):

        self.view = dc.spinUpManyContainers(dockerBuildTag, hostIp, networkIpPrefix, port_prefix, 2)

        for container in self.view:
            if " " in container["containerID"]:
                self.assertTrue(False, "There is likely a problem in the settings of your ip addresses or network.")

    def tearDown(self):
        print()
        # dc.cleanUpDockerContainer()


    def getPayload(self, ipPort, key):
        response = checkKey(ipPort, key, {})
        #print(response)
        data = response.json()
        return data["payload"]

    def confirmAddKey(self, ipPort, key, value, expectedStatus, expectedMsg, expectedReplaced, payload={}):
        response = storeKeyValue(ipPort, key, value, payload)

        #print(response)

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
        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        print("Response is", data)
        self.assertEqual(data['result'], expectedResult)
        if expectedValue != None and 'value' in data:
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

        self.assertTrue(viewMatch(data['view'], expectedView), "%s != %s"%(data['view'], expectedView))

    def confirmAddNode(self, ipPort, newAddress, expectedStatus, expectedResult, expectedMsg):
        response = addNode(ipPort, newAddress)

        #print(response)

        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['result'], expectedResult)
        self.assertEqual(data['msg'], expectedMsg)

    def confirmDeleteNode(self, ipPort, removedAddress, expectedStatus, expectedResult, expectedMsg):
        response = removeNode(ipPort, removedAddress)
        print("IpPort: ", ipPort)
        # print(response)
        print("response.text: ", response.text)
        self.assertEqual(response.status_code, expectedStatus)

        data = response.json()
        self.assertEqual(data['result'], expectedResult)
        self.assertEqual(data['msg'], expectedMsg)

    def concurrentStoreKeyValue(self, urlList):
        # for byte in result:
        #     data = byte.decode('utf8').replace("'", '"')
        #     print(json.loads(data))

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(urlList))
        res = loop.run_until_complete(future)  
        return res


##########################################################################################################

    # def test_a_add_key_value_one_node(self):
    #     key = "addNewKey"
    #     val = ["Golang", "Python", "JavaScript"]
    #     urlList = []
    #     for i in range(3):
    #         url = [self.view[i]["testScriptAddress"], key, val[i], {}]
    #         urlList.append(url)
    #     res = self.concurrentStoreKeyValue(urlList=urlList)
    #     putRes = []
    #     for byte in res:
    #         data = byte.decode('utf8').replace("'", '"')
    #         putRes.append(json.loads(data))
        
    #     results = []
    #     for i in range(3):
    #         results.append(getKeyValue(ipPort=self.view[i]["testScriptAddress"], key=key, payload=putRes[i]).json()["value"])
    #     print(results)

    #     self.assertEqual(results[0], results[1])
    #     self.assertEqual(results[1], results[2])
    #     self.assertEqual(results[0], results[2])
    def test_a_add_key_value_one_node(self):
        key = ["George", "Michael"]
        val = ["golang", "python"]
        resPut = []
        # dc.partittionContainer(self.view[1]["containerID"])
        resPut.append(storeKeyValue(self.view[0]["testScriptAddress"], key[0], val[0], {}).json())
        resPut.append(storeKeyValue(self.view[0]["testScriptAddress"], key[1], val[1], {}).json())
        # dc.unpartittionContainer(self.view[1]["containerID"])
        # self.confirmGetKey(ipPort=self.view[1]["testScriptAddress"], 
        #                     key=key,
        #                     expectedStatus=200,
        #                     expectedResult="Success",
        #                     expectedValue=val[0],
        #                     payload=resPut[0]["payload"])        
        dc.runCommandLine(["docker", "logs", "-f", self.view[1]["containerID"]])
        
           


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestHW3.BUILD = sys.argv.pop()
    else: 
        TestHW3.BUILD = "nil"
    unittest.main() 
