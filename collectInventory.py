import sys,os,time,paramiko

#import modules for test
sys.path.append("C:\Automation\Modules\BMC\LogCollection")
sys.path.append("C:\Automation\Modules\BMC\Lan")
sys.path.append("C:\Automation\Modules\BMC\Basic")
sys.path.append("C:\Automation\Modules\Redfish\LogCollection")
sys.path.append("C:\Automation\Modules\general")

import clearSELLog,getBMCLog,pathDefine
import getLanInfo,RedfishCommand,sshConnect
import basicCheck,testCaseOutputFormat,testCaseGetLog,getFWVersion,fileHandle



#getting parameter from Jenkins

BMC_ip=os.getenv("BMC_ip")
BMC_user=os.getenv("BMC_user")
BMC_pwd=os.getenv("BMC_pw")
Ciphersuite=os.getenv("Ciphersuite")
OS_ip=os.getenv("OS_ip")
OS_user=os.getenv("OS_user")
OS_pwd=os.getenv("OS_pw")
Test_via_Redfish=os.getenv("Test_via_Redfish")
Test_via_IPMI=os.getenv("Test_via_IPMI")


#Default is 5s
ipmi_press_time=5

ipmiDict={}
ipmiDict['bmcUser'] = f' -U {BMC_user}'
ipmiDict['bmcPwd'] = f' -P {BMC_pwd}'
ipmiDict['bmcIP'] = f' -H {BMC_ip}'    
ipmiDict['command'] = f' -C {Ciphersuite}'


#Variables for record
failRecord = []	

'''
Define Function
'''

def gapTime(waitTime):
    testCaseOutputFormat.StepGapTimeHead(waitTime)
    testCaseOutputFormat.StepGapTimeBody()
    testCaseOutputFormat.StepGapTimeFoot(waitTime)

def checkInfo():  
    checkStatus=1    
    #Check if OS IP is available
    if basicCheck.checkBMC(BMC_ip) == 0:
        print(f"[Failed] Ping BMC failed.")
        sys.exit(-1)
        
    if basicCheck.checkLoginBMC(ipmiDict) == 0:
        print(f"[Failed] Login BMC failed.")
        sys.exit(-1)

    if basicCheck.checkOS(OS_ip) == 0:
        print(f"[Log] Ping OS failed.")
        sys.exit(-1) 

    if basicCheck.checkLoginOS(OS_ip,OS_user,OS_pwd) == 0:
        print(f"[Log] Login OS failed.")
        sys.exit(-1)
        
    goldenBMCVersion = getFWVersion.BMCVersion(ipmiDict)
    if goldenBMCVersion == 0:
        print("[Failed] Get BMC version.")
        sys.exit(-1)

    goldenBIOSVersion = getFWVersion.BIOSVersion(OS_ip,OS_user,OS_pwd)         
    if goldenBIOSVersion == 0:
        print("[Failed] Get BIOS version.")
        sys.exit(-1)
    return [checkStatus,goldenBMCVersion,goldenBIOSVersion]

def saveFailRecord(ipmiInfo,logPath,failRecordList,cycle):
    testCaseGetLog.getLogBMC(ipmiInfo,cycle,logPath,failRecordList)
    testCaseGetLog.getLogRedfish(ipmiInfo,cycle,logPath,failRecordList)
    if len(failRecordList)>0:
        fileHandle.fileLogList(logPath,'failRecord',failRecordList)
        time.sleep(3)
        failRecordList.clear()
        

'''
TC Functions
'''

def collectInventoryRedfish(ipmiInfo):
   
    PSB_id=1
    testCaseID='68999'
    testCaseTitle='Access Redfish via Dedicated BMC Network'

    getResult = ['Fail','Fail','Fail','Fail','Fail','Fail','Fail']

    validateCommand='/Chassis/Self'
    #1. GET https://<BMC_IP>/redfish/v1/Chassis/Self
    PSB = f'GET https://<BMC_IP>/redfish/v1/Chassis/Self'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[0]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[0],setMessage,1)

    PSB_id = PSB_id + 1

    validateCommand='/Chassis/Self/PCIeDevices'
    #2. GET https://<BMC_IP>/redfish/v1/Chassis/Self/PCIeDevices
    PSB = f'GET https://<BMC_IP>/redfish/v1/Chassis/Self/PCIeDevices'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[1]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[1],setMessage,1)

    PSB_id = PSB_id + 1

    validateCommand='/Chassis/Self/NetworkAdapters'
    #3. GET https://<BMC_IP>/redfish/v1/Chassis/Self/NetworkAdapters
    PSB = f'GET https://<BMC_IP>/redfish/v1/Chassis/Self/NetworkAdapters'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[2]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[2],setMessage,1)

    PSB_id = PSB_id + 1

    validateCommand='/Chassis/Self/MediaControllers'
    #4. GET https://<BMC_IP>/redfish/v1/Chassis/Self/MediaControllers
    PSB = f'GET https://<BMC_IP>/redfish/v1/Chassis/Self/MediaControllers'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[3]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[3],setMessage,1)

    PSB_id = PSB_id + 1

    validateCommand='/Chassis/Self/PCIeSlots'
    #5. GET https://<BMC_IP>/redfish/v1/Chassis/Self/PCIeSlots
    PSB = f'GET https://<BMC_IP>/redfish/v1/Chassis/Self/PCIeSlots'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[4]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[4],setMessage,1)

    PSB_id = PSB_id + 1

    validateCommand='/Systems/Self/Processors'
    #6. GET https://<BMC_IP>/redfish/v1/Systems/Self/Processors
    PSB = f'GET https://<BMC_IP>/redfish/v1/Systems/Self/Processors'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[5]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[5],setMessage,1)

    PSB_id = PSB_id + 1

    validateCommand='/Systems/Self/Storage'
    #7. GET https://<BMC_IP>/redfish/v1/Systems/Self/Storage
    PSB = f'GET https://<BMC_IP>/redfish/v1/Systems/Self/Storage'
    setMessage= ''
    
    testCaseOutputFormat.testCaseOutputHead(PSB_id,testCaseID,testCaseTitle,PSB,1)    

    redfishGet = RedfishCommand.RedfishGetCommand(BMC_ip,BMC_user,BMC_pwd,pathDefine.redFishPrefix()+validateCommand)
    if redfishGet[0] == -1:
        setMessage=f" {validateCommand} GET resuilt: {redfishGet[1]}\n"
        resultBody=f"[Fail] {validateCommand} GET resuilt: {redfishGet[1]}\n"
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        testCaseOutputFormat.testCaseOutputBody(f'[Log] Success to GET from Redfish API.\n')
        print(redfishGet[1])
        getResult[6]='Pass'
    
    testCaseOutputFormat.testCaseOutputFoot(PSB_id,getResult[6],setMessage,1)

    
    return getResult


def collectInventoryIPMI(ipmiInfo):
    
    testCaseID='68969'
    testCaseTitle='Collect Inventory via IPMI'

    PSB = f'ipmitool -I lanplus -H <BMC_IP> -U <username> -P <password> fru print'
    setMessage= ''
    getInfoResult = 'Fail'
    testCaseOutputFormat.testCaseOutputHead(1,testCaseID,testCaseTitle,PSB,1)

    fruPrint = getBMCLog.returnBMCLog(ipmiInfo,'fru print')
    if fruPrint==0:
        setMessage = f'failed using IPMI command fru print.\n'
        resultBody = f'[Fail] failed using IPMI command fru print.\n'
        testCaseGetLog.appendRecord(failRecord,setMessage)
    else:
        print(fruPrint)
        if 'FRU Device Description' in fruPrint:
            resultBody = f'[Log] get inventory information with IPMI command fru print.\n'
            getInfoResult = 'Pass'
        else:
            setMessage = f'no inventory information returned after fru print.\n'
            resultBody = f'[Fail] no inventory information returned after fru print.\n'
            testCaseGetLog.appendRecord(failRecord,setMessage)
            
    testCaseOutputFormat.testCaseOutputBody(resultBody)
    testCaseOutputFormat.testCaseOutputFoot(1,getInfoResult,setMessage,1)

    return [getInfoResult]
    
if __name__ == '__main__':

    

    #Basic check: BMC IP, OS IP, BMC account/password
    #make sure test environment is ready for automation
    testCaseOutputFormat.basicCheckOutputHead()
    checkInfoStatus = checkInfo()
    testCaseOutputFormat.basicCheckOutputFoot()

    #Create Log folder
    logFolderPath = testCaseGetLog.logFolderGenerate(f'Access-Network')
    logPath=logFolderPath[0]
    comparePath=logFolderPath[1]
    sysInfoPath=logFolderPath[2]
    selErrorInfoPath=logFolderPath[3]
    systemInfoPath=logFolderPath[4]

    #Get Gold Sample
    godlenSampleStatus = testCaseGetLog.getGolden(ipmiDict,OS_ip,OS_user,OS_pwd,comparePath,sysInfoPath,checkInfoStatus[1],checkInfoStatus[2])

    ipmiResult = []
    Test_duration_ipmi = 0
    if Test_via_IPMI == 'Yes':
        start_time = time.time()
        ipmiResult = collectInventoryIPMI(ipmiDict)
        Test_duration_ipmi = max(round(time.time() - start_time),1)

    redfishResult = []
    Test_duration_redfish = 0
    if Test_via_Redfish == 'Yes':
        start_time = time.time()
        redfishResult = collectInventoryRedfish(ipmiDict)
        Test_duration_redfish = max(round(time.time() - start_time),1)

    
    #Test Result
    
    testCaseOutputFormat.resultOutputHead()   
    testResult = []
    if Test_via_IPMI == 'Yes':
        testResult.append(f'Collect Inventory via IPMI: {Test_duration_ipmi} seconds')
        testResult.append(f'PSB ID: 1 PASS:{1 if ipmiResult[0] == "Pass" else 0} FAIL: {1 if ipmiResult[0] == "Fail" else 0}')
        
    if Test_via_Redfish == 'Yes':
        testResult.append(f'Collect Inventory through Various Redfish APIs: {Test_duration_redfish} seconds')
        testResult.append(f'PSB ID: 1 PASS:{1 if redfishResult[0] == "Pass" else 0} FAIL: {1 if redfishResult[0] == "Fail" else 0}')
        testResult.append(f'PSB ID: 2 PASS:{1 if redfishResult[1] == "Pass" else 0} FAIL: {1 if redfishResult[1] == "Fail" else 0}')
        testResult.append(f'PSB ID: 3 PASS:{1 if redfishResult[2] == "Pass" else 0} FAIL: {1 if redfishResult[2] == "Fail" else 0}')
        testResult.append(f'PSB ID: 4 PASS:{1 if redfishResult[3] == "Pass" else 0} FAIL: {1 if redfishResult[3] == "Fail" else 0}')
        testResult.append(f'PSB ID: 5 PASS:{1 if redfishResult[4] == "Pass" else 0} FAIL: {1 if redfishResult[4] == "Fail" else 0}')
        testResult.append(f'PSB ID: 6 PASS:{1 if redfishResult[5] == "Pass" else 0} FAIL: {1 if redfishResult[5] == "Fail" else 0}')
        testResult.append(f'PSB ID: 7 PASS:{1 if redfishResult[6] == "Pass" else 0} FAIL: {1 if redfishResult[6] == "Fail" else 0}')
        
    testResult.append(f'The Log will be stored at: {logPath}')
    
    testCaseOutputFormat.resultOutputBody(testResult)

    if len(failRecord)>0:
        fileHandle.fileLogList(logPath,'failRecord',failRecord)
        print(f'Record Fail Cycle on {logPath}failRecord.txt.')

    testCaseOutputFormat.resultOutputFoot()

    if Test_via_Redfish == 'Yes':
        if 'Fail' in redfishResult:
            sys.exit(-1)
    if Test_via_IPMI == 'Yes':
        if 'Fail' in ipmiResult:
            sys.exit(-1)




