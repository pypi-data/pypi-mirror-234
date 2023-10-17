from py5paisa import FivePaisaClient

def fivepaisalogin():
    ############## Login into 5Paisa Account Swapna ###################
    
    cred={
        "APP_NAME":"5P50222634",
        "APP_SOURCE":"16397",
        "USER_ID":"KuLeolmFxYn",
        "PASSWORD":"buPwfrtC5RX",
        "USER_KEY":"N4ETSSr1m6Swfd4efeeoenBlYcxDOLeX",
        "ENCRYPTION_KEY":"zfsjTxU7NDy1oItYYVYr5EZlKbpv5bkj"
        }

    totp=input("input totp: ")

    client = FivePaisaClient(cred=cred)
    # New TOTP based authentication
    #client.get_totp_session('Your ClientCode','TOTP from authenticator app','Your Pin')
    client.get_totp_session(50222634,str(totp),147258)
    return client

## To generate Token
## https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey=N4ETSSr1m6Swfd4efeeoenBlYcxDOLeX&ResponseURL=https://www.5paisa.com/technology/developer-apis
##Client = FivePaisaClient(cred=cred)
##Client.get_access_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwNTg1ODA3Iiwicm9sZSI6Ik40RVRTU3IxbTZTd2ZkNGVmZWVvZW5CbFljeERPTGVYIiwibmJmIjoxNjg2MDIxODIxLCJleHAiOjE2ODYwMjE4NTEsImlhdCI6MTY4NjAyMTgyMX0.uU_jeye0QPopDQWhA88-dm5VehjAyZhqMt0a9ZA--n0')