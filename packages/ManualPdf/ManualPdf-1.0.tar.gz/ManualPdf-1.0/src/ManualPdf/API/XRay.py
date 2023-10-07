import json
import requests
from FPDFv1.Utilities import Essentials


class XRay:

    def __init__(self,url,username,pwd,test_id,test_exe_id):
        self.essential = Essentials.Essentials()
        self.base_url = url
        self.username = username
        self.password = pwd
        self.Test_key = test_id
        self.Execution_key = test_exe_id
        self.headers = {'Content-Type': 'application/json'}

    def get_testrun_details(self, Test_key, Execution_key):
        testrun_url = self.base_url + "/rest/raven/2.0/api/testrun?" + \
                      "testExecIssueKey=" + Execution_key.strip() + \
                      "&testIssueKey=" + Test_key.strip()
        response = requests.get(testrun_url, headers=self.headers, auth=(self.username, self.password))
        data = response.json()
        return data

    def get_step_details(self, test_run_id):
        testrun_url = self.base_url + "/rest/raven/2.0/api/testrun/" + test_run_id + "/step"
        response = requests.get(testrun_url, headers=self.headers, auth=(self.username, self.password))
        data = response.json()
        return data

    def get_test_case_details(self, testcase_key):
        testcase_url = self.base_url + "/rest/api/2/issue/" + testcase_key

        response = requests.get(testcase_url, headers=self.headers, auth=(self.username, self.password))
        data = response.json()
        return data

    def get_name_from_username(self, username):
        url = self.base_url + "/rest/api/2/user?username=" + username

        response = requests.get(url, headers=self.headers, auth=(self.username, self.password))
        data = response.json()['displayName']
        data = data.split('[')[0]
        return data

    def get_file_data(self, url):
        response = requests.get(url, auth=(self.username, self.password), allow_redirects=True)
        return response.content

    def upload_attachment(self, test_run_id, attachment_path):
        attachment_url = self.base_url + "/rest/raven/2.0/api/testrun/" + str(test_run_id)
        base64_data = self.essential.img_encode(attachment_path)
        file_name = attachment_path.rsplit('\\', 1)[1]
        values = json.dumps({
            "evidences": {
                "add": [
                    {
                        "data": base64_data,
                        "filename": file_name,
                        "contentType": "application/pdf"
                    }]
            }
        })

        response = requests.put(attachment_url, data=values, headers=self.headers,
                                auth=(self.username, self.password))

    def update_label(self, test_run_id):
        testrun_url = self.base_url + "/rest/api/2/issue/" + str(test_run_id)
        new_labels = ["ManualPDF"]

        payload = {
            "update": {
                "labels": [{"add": label} for label in new_labels]
            }
        }

        response = requests.put(testrun_url, json=payload, headers=self.headers,
                                auth=(self.username, self.password))

    def update_comment(self, test_run_id, test_case_key):
        testrun_url = self.base_url + "/rest/api/2/issue/" + str(test_run_id) + "/comment"
        comment_text = "Custom execution pdf is attached to key : " + test_case_key

        payload = {
            "body": comment_text
        }

        response = requests.post(testrun_url, json=payload, headers=self.headers,
                                 auth=(self.username, self.password))
