from FPDFv1.API.XRay import XRay
from FPDFv1.Utilities import Essentials
import os
import jinja2
import pdfgen


class CreateExecutionReport:

    def __init__(self,url,username,pwd,test_id,test_exe_id):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.sep.join([self.dir_path, "Templates"]) + os.sep
        self.template_loader = jinja2.FileSystemLoader(searchpath=self.template_path)
        self.template_env = jinja2.Environment(loader=self.template_loader, autoescape=True)
        self.filename = None
        self.testrun_id = None
        self.base_url = url
        self.username = username
        self.password = pwd
        self.Test_key = test_id
        self.Execution_key = test_exe_id

    def create_html(self, test_case_key):

        print("**** Accelerator Execution In progress... ****")
        xray = XRay(self.base_url,self.username,self.password,self.Test_key,self.Execution_key)
        essentials = Essentials.Essentials()
        testrun_details = xray.get_testrun_details(self.Test_key, self.Execution_key)

        self.testrun_id = testrun_details['id']
        step_details = xray.get_step_details(str(self.testrun_id))
        case_details = xray.get_test_case_details(test_case_key)

        directory = self.dir_path + "\\tmp"
        if not os.path.exists(directory):
            os.makedirs(directory)
        cleaned_string = essentials.remove_special_characters(str(case_details['fields']['summary']))
        html_file = open(directory + "\\" + cleaned_string + ".html", "w")
        self.filename = cleaned_string + ".html"

        header = self.template_env.get_template('browserheader.html')
        output = header.render()
        html_file.write(output)
        footer = self.template_env.get_template('footer.html')
        output = footer.render(report_version='1.0')
        html_file.write(output)
        heading = self.template_env.get_template('heading.html')
        try:
            output = heading.render(TCName=test_case_key, ExecID=self.Execution_key,
                                    var=', '.join(case_details['fields']['labels']),
                                    executed=xray.get_name_from_username(testrun_details['executedBy']),
                                    USId=case_details['fields']['issuelinks'][0]['outwardIssue']['key'],
                                    Overall_status=testrun_details['status'],
                                    Test_Objective=case_details['fields']['description'],
                                    Test_Name=case_details['fields']['summary'],
                                    env=case_details['fields']['environment'],
                                    Overall_test_start=essentials.utc_time_print(testrun_details['startedOn']),
                                    Overall_end_start=essentials.utc_time_print(testrun_details['finishedOn']),
                                    Timediff=essentials.utc_time_dff(testrun_details['startedOn'],
                                                                     testrun_details['finishedOn']))
        except KeyError:
            output = heading.render(TCName=test_case_key, ExecID=self.Execution_key,
                                    var=', '.join(case_details['fields']['labels']),
                                    executed=xray.get_name_from_username(testrun_details['executedBy']),
                                    USId=case_details['fields']['issuelinks'][0]['inwardIssue']['key'],
                                    Overall_status=testrun_details['status'],
                                    Test_Objective=case_details['fields']['description'],
                                    Test_Name=case_details['fields']['summary'],
                                    env=case_details['fields']['environment'],
                                    Overall_test_start=essentials.utc_time_print(testrun_details['startedOn']),
                                    Overall_end_start=essentials.utc_time_print(testrun_details['finishedOn']),
                                    Timediff=essentials.utc_time_dff(testrun_details['startedOn'],
                                                                     testrun_details['finishedOn']))
        html_file.write(output)

        for step_item in step_details:
            actual_result = step_item['actualResult']['raw'] if 'raw' in step_item['actualResult'] else ""
            step_details = self.template_env.get_template('step.html')
            output = step_details.render(TestStep=step_item['fields']['Action']['value']['raw'],
                                         ExpectedResult=step_item['fields']['Expected Result']['value']['raw'],
                                         ActualResult=actual_result,
                                         teststatus=step_item['status'],
                                         stepcount=step_item['index'])
            html_file.write(output)

            step_evidence = step_item['evidences']
            for evidence in step_evidence:
                file_data = xray.get_file_data(evidence['fileURL'])
                attachment_detail = self.template_env.get_template('screenshot.html')
                output = attachment_detail.render(screenname=evidence['fileName'],
                                                  image=essentials.data_encode(file_data))
                html_file.write(output)

        html_file.close()

    def convert_to_pdf(self, test_case_key):
        # convert to pdf
        xray = XRay(self.base_url,self.username,self.password,self.Test_key,self.Execution_key)
        file_path = self.dir_path + "\\tmp\\" + self.filename
        pdf_file_name = file_path.replace(".html", ".pdf")
        pdfgen.sync.from_file(file_path, pdf_file_name)
        xray.upload_attachment(self.testrun_id, pdf_file_name)
        print("PDF is uploaded to Execution Instance : ", self.Execution_key)
        xray.update_label(self.Execution_key)
        xray.update_comment(self.Execution_key, test_case_key)


# url=username=pwd=testid=test_exe_id=""
# obj = CreateExecutionReport(url,username,pwd,testid,test_exe_id)
obj= CreateExecutionReport('https://dev.jira.jnj.com',"ssomasu3","mylogin@jnj#123","JCRC-1138","JCRC-1144")
# n = len(obj.Test_key.split(","))
# print("Total Tests identified to upload PDF report : ", n)
# for TC in obj.Test_key.split(","):
#     obj.create_html(TC)
#     obj.convert_to_pdf(TC)
# print("========== END ==========")
