import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from simple_salesforce import Salesforce,SalesforceLogin


def assign_sf_login(Login_Details,env):
    username = Login_Details[env]['username']
    password = Login_Details[env]['password']
    api_password = Login_Details[env]['password']+Login_Details[env]['security_token']
    organizationId = Login_Details[env]['orgid']
    security_token = Login_Details[env]['security_token']
    instance_url = Login_Details[env]['instance_url']
    consumer_key = Login_Details[env]['consumer_key']
    consumer_Secret = Login_Details[env]['consumer_Secret']
    sf=Salesforce(username=username, password=api_password, domain='test', organizationId=organizationId)
    #sf = Salesforce(instance=instance_url, session_id='')
    #sf = Salesforce(username=username, password=password, security_token=security_token)
    #sf = Salesforce(username=username, password=password,  organizationId=organizationId)
    #sf = Salesforce(username=username, password=password, security_token=security_token, domain='test')
    #sf=Salesforce(username=username, password=api_password, domain='test', organizationId=organizationId)
    #sf = Salesforce(username=username, password=api_password, security_token=security_token)
    #sf = Salesforce(username=username, password=api_password,  organizationId=organizationId)
    #sf = Salesforce(username=username, password=api_password, security_token=security_token, domain='test')
    #sf=Salesforce(username=username, password=api_password, domain='test', organizationId=organizationId , security_token= '' )

    #sf=Salesforce(username=username, password=password, consumer_key='3MVG9onPgXc8rMW7AceM0I2Bo6_b_xNe1_zQl_BnZSGs8uIapsmasy7KcWPm2NltdCvuTeOek7oJyznGho7sw',consumer_secret= 'BC38265FE4DE6DE83A55EAC1710A41984D3DF61159C61BD509E4C988460A8A5F' ,domain='test' )

    #sf = Salesforce(username=username, password=password, security_token=security_token,  sandbox=True)
    #sf = Salesforce(username=username, password=api_password, security_token=security_token,domain='test')
    #sf=Salesforce(username=username, password=api_password, domain='test', organizationId=organizationId)
    #sf=Salesforce(username=username, password=api_password, sandbox = True, organizationId=organizationId)
    #sf=Salesforce(username=username, password=password, sandbox = False, security_token=security_token)
    #session_id,instance = SalesforceLogin(username=username, password=password, security_token=security_token,domain='test')
    #sf,a=SalesforceLogin(username=username, password=api_password, domain='test', organizationId=organizationId)



    return sf
