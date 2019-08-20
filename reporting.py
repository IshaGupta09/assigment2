import requests
import json
import time
import csv

def generateSessionId():
    baseURL = "https://api.inmobi.com/v1.0/generatesession/generate"
    headers = {
        "secretKey": "ce974ad22a0446f38dc03fe8647cb343",
        "username": "ishag905@gmail.com",
        "password": "Testing@12345",
    }
    response = requests.get(baseURL,headers=headers)
    responseJson = json.loads(response.content)
    return responseJson['respList'][0]['sessionId']

def getPerformanceReport(sessionId):
    baseURL = "http://api.inmobi.com/reporting/performance"
    headers = {
        "accountid": "1c0e67a62b364ad9a2b54f5d64d6cf54",
        "secretkey": "ce974ad22a0446f38dc03fe8647cb343",
        "sessionid": sessionId
    }
    startdate = "2019-08-01"
    enddate = "2019-08-09"
    columns = "day,advertiser_account,advertiser_app_id,campaign,campaign_id,clicks,spend"
    response = requests.get(baseURL+"?start="+startdate+"&end="+enddate+"&columns="+columns, headers = headers)
    # print (response.content)
    responseJson = json.loads(response.content)
    return responseJson['data']['resource_info'][0]['job_id']

def checkJobStatus(jobId,sessionId):
    baseURL = "http://api.inmobi.com/reporting/performance/job_info?job_id="+jobId
    headers = {
        "accountid": "1c0e67a62b364ad9a2b54f5d64d6cf54",
        "secretkey": "ce974ad22a0446f38dc03fe8647cb343",
        "sessionid": sessionId
    }
    response = requests.get(baseURL, headers = headers)
    responseJson = json.loads(response.content)
    return responseJson['data']['final_job_status']['status']

def getJobData(jobId,sessionId):
    baseURL = "http://api.inmobi.com/reporting/performance/download?job_id="+jobId
    headers = {
        "accountid": "1c0e67a62b364ad9a2b54f5d64d6cf54",
        "secretkey": "ce974ad22a0446f38dc03fe8647cb343",
        "sessionid": sessionId
    }
    response = requests.get(baseURL, headers = headers)
    responseJson = json.loads(response.content)
    return responseJson



sessionId = generateSessionId()
JobId = getPerformanceReport(sessionId)

JobStatus = "InProgress"
while (JobStatus == "InProgress"):
    JobStatus = checkJobStatus(JobId, sessionId)
    time.sleep(5)

data = getJobData(JobId,sessionId)
