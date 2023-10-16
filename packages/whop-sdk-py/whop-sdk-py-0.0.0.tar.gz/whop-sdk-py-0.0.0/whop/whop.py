import requests, json, platform

class Whop:
    def __init__(self, apiKey, useHWID=True):
        self.baseUrl = "https://api.whop.com/v2/"
        self.headers = {
            'Authorization': "Bearer " + apiKey,
            'Content-Type': 'application/json'
        }
        self.useHWID = useHWID
        self.errorText = 'Your access token is invalid. Please make sure you are passing an access token, and that it is correctly formatted.'

    def hwid(self):
        return platform.node()

    def updateLicense(self, membership_id, updated_payload):
        payload = updated_payload

        req = requests.post(
    		f"https://api.whop.com/api/v2/memberships/{membership_id}",
    		headers=self.headers,
    		json=payload
    	)
        if req.status_code == 200:
            return True, req.json()

        return False, req.json()

    def validateLicense(self, membership_id, metadata=None):
        url = f'{self.baseUrl}/memberships/{membership_id}/validate_license'

        if self.useHWID == True:
            payload = {
                'metadata': {
                    'hwid': self.hwid()
                }
            }
        else:
            if metadata is None:
                return {"error": "you tried to use custom metdata but did not set useHWID to False"}

            payload = {
                'metadata': metadata
            }

        response = requests.post(url, headers=self.headers, json=payload)
        if self.errorText in response.text:
            return False, {"error": "Invalid API Key"}
        if response.status_code == 201:
            return True, response.json()
        elif response.status_code == 404:
            return False, {"error": "License Not Found"}
        elif 'Please reset your key to use on a new machine' in response.text:
            self.updateLicense(membership_id, payload)
        else:
            return False, {"error": f'Failed to validate license: {response.text}'}

    def retreiveMembership(self, membership_id):
        url = f"{self.baseUrl}/memberships/{membership_id}"

        res = requests.get(url, headers=self.headers)
        if self.errorText in res.text:
            return {"error": "Invalid API Key"}
        elif res.status_code == 404:
            return {"error": "License Not Found"}

        return res.json()

    def getMemberID(self, license):
        url = f"{self.baseUrl}/memberships/{license}"

        res = requests.get(url, headers=self.headers)
        if self.errorText in res.text:
            return {"error": "Invalid API Key"}
        elif res.status_code == 404:
            return {"error": "License Not Found"}

        return res.json()['id']


    def cancelMembership(self, membership_id):
        url = f"{self.baseUrl}/memberships/{membership_id}/cancel"

        res = requests.post(url, headers=self.headers)

        return res.json()

    def addFreeDays(self, membership_id, days):
        url = f"{self.baseUrl}/memberships/{membership_id}/add_free_days"

        res = requests.post(url, headers=self.headers, json={"days": int(days)})
        if res.status_code == 201:
            return {"success": True}
        else:
            return res.json()
