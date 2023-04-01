import json

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth


class Searcher():
    def __init__(self):
        self.get_identity_id()
        self.get_aws_config()

    def get_identity_id(self):
        headers = {
            "authority": "cognito-identity.us-east-2.amazonaws.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4",
            "amz-sdk-invocation-id": "e611edc8-604a-47ed-a3d0-2d4e4fe8e3af", # Is this ok to have hardcoded invocation id?
            "amz-sdk-request": "attempt=1; max=3",
            "cache-control": "no-cache",
            "content-type": "application/x-amz-json-1.1",
            "dnt": "1",
            "origin": "https://www.aircanada.com",
            "pragma": "no-cache",
            "referer": "https://www.aircanada.com/",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
            "x-amz-target": "AWSCognitoIdentityService.GetId",
            "x-amz-user-agent": "aws-sdk-js/3.6.1 os/macOS/10.15.7 lang/js md/browser/Microsoft_Edge_110.0.1587.41 api/cognito_identity/3.6.1 aws-amplify/3.8.23_js"
        }
        url = "https://cognito-identity.us-east-2.amazonaws.com/"
        data = {"IdentityPoolId":"us-east-2:4a7f6b48-a8ab-499b-9e7f-31e79b54638e"}
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        self.identity_id = response_json["IdentityId"]

    def get_aws_config(self):
        headers = {
            "authority": "cognito-identity.us-east-2.amazonaws.com",
            # "scheme": "https",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4",
            # "amz-sdk-invocation-id": "67b81d93-3731-40a2-86ca-7b7af5160447",
            "amz-sdk-invocation-id": "e611edc8-604a-47ed-a3d0-2d4e4fe8e3af", # Is this ok to have hardcoded invocation id?
            "amz-sdk-request": "attempt=1; max=3",
            "cache-control": "no-cache",
            "content-type": "application/x-amz-json-1.1",
            "dnt": "1",
            "origin": "https://www.aircanada.com",
            "pragma": "no-cache",
            "referer": "https://www.aircanada.com/",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
            "x-amz-target": "AWSCognitoIdentityService.GetCredentialsForIdentity",
            "x-amz-user-agent": "aws-sdk-js/3.6.1 os/macOS/10.15.7 lang/js md/browser/Microsoft_Edge_110.0.1587.41 api/cognito_identity/3.6.1 aws-amplify/3.8.23_js"
        }
        url = "https://cognito-identity.us-east-2.amazonaws.com/"
        data = {
            # "IdentityId": "us-east-2:6d8b1368-8473-471f-abf1-a236acac70e2"
            "IdentityId": self.identity_id
        }
        # "IdentityId": "us-east-2:7f9c31d7-d242-4f7e-afda-916b8c6c2b9c"
        response = requests.post(url, headers=headers, json=data)
        r1 = response.json()
        self.access_key_id = r1['Credentials']['AccessKeyId']
        self.secret_key = r1['Credentials']['SecretKey']
        self.session_token = r1['Credentials']['SessionToken']

    def get_auth(self):
        return AWSRequestsAuth(aws_access_key=self.access_key_id,
                               aws_secret_access_key=self.secret_key,
                               aws_host='api-gw.dbaas.aircanada.com',
                               aws_region='us-east-2',
                               aws_service='execute-api',
                               aws_token=self.session_token)

    def get_market_token(self, ori: str, des: str, date: str):
        headers = {
            "authority": "akamai-gw.dbaas.aircanada.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4",
            #"ama-client-ref": "92a6f456-b299-43ab-a9fb-7e3d865f0198",
            "ama-client-ref": "27e5aa13-71a3-4a20-99df-325963f2713e", # Is this ok to have hardcoded client reference?
            # "authorization": "AWS4-HMAC-SHA256 Credential=/20230211/us-east-2/execute-api/aws4_request, SignedHeaders=host;x-amz-date;x-amz-security-token, Signature=2709f3e61806c689840c68b3e1b4770f03eac1fa816998561f599d1b27909e3d",
            # "authorization": "AWS4-HMAC-SHA256 Credential=/20230314/us-east-2/execute-api/aws4_request, SignedHeaders=host;x-amz-date;x-amz-security-token, Signature=755d1657795486f098fc76cce7801fafbafc0983efc883ce68ae7bac1ae03faa",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.aircanada.com",
            "pragma": "no-cache",
            "referer": "https://www.aircanada.com/",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
            # "x-amz-date": x_amz_date,
            # "x-amz-security-token": x_security_token,
            "x-api-key": "Z5R8Rm1sA37iC0gaS5kb69ltHwKBTYzUa89gQDwm"
        }
        url = "https://akamai-gw.dbaas.aircanada.com/loyalty/dapidynamic/1ASIUDALAC/v2/reward/market-token"
        data = {
            "itineraries": [
                {
                    "originLocationCode": ori,
                    "destinationLocationCode": des,
                    "departureDateTime": date
                }
            ],
            "countryOfResidence": "CA"
        }
        # data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers, json=data, auth=self.get_auth())
        r1 = response.json()
        self.ama_session_token = r1['data']['sessionToken']

    def get_air_bounds(self, ori: str, des: str, date: str, ac_searcher_cabin_class: list) -> requests.Response:
        headers = {
            "authority": "akamai-gw.dbaas.aircanada.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4",
            # "ama-client-ref": "d662a606-ad1a-4254-994c-13019c734d25",
            "ama-client-ref": "27e5aa13-71a3-4a20-99df-325963f2713e", # Is this ok to have hardcoded reference id?
            "ama-session-token": self.ama_session_token,
            # "authorization": "AWS4-HMAC-SHA256 Credential=ASIAWBHE22QVOHXZQH7O/20230211/us-east-2/execute-api/aws4_request, SignedHeaders=host;x-amz-date;x-amz-security-token, Signature=337881519b12f5742a1361974ec66f06d5ce7b0abb8f0d1919a70bdd7f34dd8c",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.aircanada.com",
            "pragma": "no-cache",
            "referer": "https://www.aircanada.com/",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
            # "x-amz-date": "20230211T121518Z",
            # "x-amz-security-token": "IQoJb3JpZ2luX2VjEDQaCXVzLWVhc3QtMiJHMEUCIQDjLNeyYuvliGkXO350xmdGobz3+Ex8wY18FllDh4WzsAIgE2hEAUabeJiHohAkj4YXmKMIh7+Pig4kceCAW/dcVvAqmwYIvf//////////ARACGgw0MTQ5NDQyNTI5NzAiDBnfZppkc2NGs9qBUirvBeP9VlxllEM1aDA6rC9kkCuZPbV2QFxounRAVakbBBY6I/GYOaOvFU5pa1khT7WUTHZSTbM9z0LG2vtnCsqYTos3Y33uq80P1+/3ZF7TP9sLanpKDjlhjVX3/baw4JhQMFGoXHkAw4J7lUJAg9wZvhRQttGkEujyz7lV8Um65V9hpQqKXmJtP0FusZ+KFdBDTR/+pK9VfaDJB6jj7Pz+xOb301kWGaFKJNOx/B4/SHM1FtMr1iWXPBTRhYvUzvFINAOkjH3zyM2+TBSnU2x+FYGJsb1rAv5IHTu5WVlW/GK/OLrOibV5mREosypfjdHp6LsRAYmjGGkMuW8TrFUSuABF0Tl8mlYcII//Xi4Puq6SXW2Bo20x/57e//4ng67ME+xh+oyTQaomLxGGj9dwNf3cn9+y+7MU8syIQMiv9tG7MhG333n9Bl6uy+mwgbUAW9pYhgLvJmZc31PYBpoQyqhdl+SgjL3NbVn5JLHY1knkHRb4lZUAZurVfLITCdt2j6fkMqrmOorsSWePJtxpQhdA+0hhjl6t79yrgOeZUsxWfQyuT177RXfyp17aAmCtP0iCtBDHaQvwzNsnqSYpF22NJJpsYEOdShovaZmAyFRmMPmdOYqmImZpdbGtWa3IQWyOjYxLzYA1sjQRsQNoo2qjcFHkfHCFpPYiRM+UooAXHwAjzwN4nAWYw0z3Xfv/XIO4blFuQY0vzheLqVss8fPRDNADYJYMf1nKU17SiFzrymaF3bAPqZ562uQnvYHv6vpWx/mqIkbmYuWu4xrx0P4ezdWBpGlJe5d1qcUp2XXz3a4e93dO64NHuVQIFhumeldGYxhmpYPq8PCi2h7I3BQdDufhRC/NZ6imrTXyTYH3MNIBMwy79hKMwW3qFMrM7JBzzuyztLPI2b4TUDUlGUXs9gDMKCz0Cmu2NFd+iOlh0XMNM6SkoROIbxrjVyiXWoKWlZGll1Oc7DTDO1AFAwyXLhlR5ViE7NeWnEGIsfMw0o2enwY6hwItWAR2ttXKDfJUkGOtl0T8lzxDaJPQHAgFd0QQoM/S/TC4t02nAoRH81UWKOQkLdzh+anmbyXmhBt9HzQ4XmPRlfCkI+mA0IFNXxqCBCl96wB/GfyIXYTbjbyqIHRkJu+fmsNf2OKJGERnENzoPWtRe3cTvG3SdsdP50GNyCEULDaJWaPEgsDDQMA1hARwE29SuxhWTaLeLkAjnBmhP0uTARtJPk+Uzprr3jA7rxFwxLBpFjUx8KPqeIVWKGatqWsEyrOZ4xos2PDST2wrmGM5JLKZmbBFAEzvwwozTYG1e6zGmny+Kfw9+hA3Goi8XRQ7d1vV0nOI/oZbJimCQcfxF2T1Bw66EQ==",
            "x-api-key": "Z5R8Rm1sA37iC0gaS5kb69ltHwKBTYzUa89gQDwm"
        }
        url = "https://akamai-gw.dbaas.aircanada.com/loyalty/dapidynamic/1ASIUDALAC/v2/search/air-bounds"
        data = {
            "searchPreferences": {
                "showSoldOut": False,
                "showMilesPrice": True
            },
            "corporateCodes": [
                "REWARD"
            ],
            "travelers": [
                {
                    "passengerTypeCode": "ADT"
                }
            ],
            "currencyCode": "CAD",
            "itineraries": [
                {
                    "originLocationCode": ori,
                    "destinationLocationCode": des,
                    "departureDateTime": date,
                    "isRequestedBound": True,
                    "commercialFareFamilies": ac_searcher_cabin_class
                }
            ]
        }
        air_bounds_response = requests.post(url, headers=headers, json=data, auth=self.get_auth())
        return air_bounds_response

    def search_for(self, ori: str, des: str, date: str, cabin_class=None):
        if cabin_class is None:
            cabin_class = [
                "ECO",
                "PREM",
                "BIZ",
                "FIRST"
            ]
        ac_searcher_cabin_class_dict = {
            "ECO": "RWDECO",
            "PREM": "RWDPRECC",
            "BIZ": "RWDBUS",
            "FIRST": "RWDFIRST"
        }
        ac_searcher_cabin_class = [ac_searcher_cabin_class_dict[x] for x in cabin_class]
        try:
            self.get_market_token(ori, des, date)
            r1 = self.get_air_bounds(ori, des, date, ac_searcher_cabin_class)
            return r1
        except:
            r1 = requests.Response
            r1.status_code = 404
            return requests.Response()
