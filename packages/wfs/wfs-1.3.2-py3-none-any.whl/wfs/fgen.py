import openpyxl
from openpyxl.styles import PatternFill, Font, Border
from openpyxl.styles.borders import Side
from openpyxl.styles import Alignment


def create_excel_sheet_results(file_path, hTitle="OneFMS - Fleet Management System", sHtitle="Url: https://onefms-uat.zig.live/"):
    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set the sheet name as "Object_repo"
    sheet.title = "Test_Results"

    # Headers for the Excel sheet
    headers = ['Tc_no', 'Features', 'UserStory', 'Test_Case', 'Test_Steps', 'Test_data',
               'Actual_Results', 'Expected_Results', 'Status', 'Screenshots', 'IncidentIds']

    # Set header values in the first row

    # Set formatting for the title row (first row)
    title_font = Font(name='Tahoma', size=20, bold=True, color="FFFFFF", underline="single")
    title_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
    title_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    title_border = Border(top=Side(border_style="thin", color="000000"),
                          left=Side(border_style="thin", color="000000"),
                          right=Side(border_style="thin", color="000000"),
                          bottom=Side(border_style="thin", color="000000"))

    # Merge and center cells for the title row (first row)
    sheet.merge_cells('A1:K1')

    # Apply formatting for the title row (first row)
    title_cell = sheet['A1']
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment
    title_cell.border = title_border
    title_cell.value = hTitle

    # Set formatting for the subtitle row (second row)
    subtitle_font = Font(name='Tahoma', size=12, bold=True, color="FFFFFF", underline="single")
    subtitle_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
    subtitle_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    subtitle_border = Border(top=Side(border_style="thin", color="000000"),
                             left=Side(border_style="thin", color="000000"),
                             right=Side(border_style="thin", color="000000"),
                             bottom=Side(border_style="thin", color="000000"))

    # Merge and center cells for the subtitle row (second row)
    sheet.merge_cells('A2:K2')

    # Apply formatting for the subtitle row (second row)
    subtitle_cell = sheet['A2']
    subtitle_cell.font = subtitle_font
    subtitle_cell.fill = subtitle_fill
    subtitle_cell.alignment = subtitle_alignment
    subtitle_cell.border = subtitle_border
    subtitle_cell.value = sHtitle

    # Set formatting for the headers (third row)
    header_font = Font(bold=True, color="FFFFFF", underline="single")
    header_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

    sheet.append(headers)
    # Apply formatting for the headers (third row)
    for cell in sheet['A3:K3'][0]:
        cell.font = header_font
        cell.fill = header_fill

    # Apply borders to the first two rows except the header row
    row_border = Border(top=Side(border_style="thin", color="000000"),
                        left=Side(border_style="thin", color="000000"),
                        right=Side(border_style="thin", color="000000"),
                        bottom=Side(border_style="thin", color="000000"))

    for row in sheet.iter_rows(min_row=2, max_row=3):
        for cell in row:
            cell.border = row_border

    # Save the Excel file
    workbook.save(file_path)


def create_excel_sheet_for_object_repo(file_path, app=None):
    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set the sheet name as "Object_repo"
    sheet.title = "Object_Repo_BasePage"

    # Headers for the Excel sheet
    if app:
        headers = ['BasePage', 'Item', 'Locators', 'Elements1', 'Action', 'Description', 'FetchElements', 'Elements2']
    else:
        headers = ['BasePage', 'Item', 'Locators', 'Elements', 'Action', 'Description', 'FetchElements']

    # Set header values in the first row
    sheet.append(headers)

    # Apply formatting to the header row (underline, bold font, white text color, and red background)
    header_font = Font(bold=True, color="FFFFFF", underline="single")
    header_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

    for cell in sheet[1]:
        cell.font = header_font
        cell.fill = header_fill

    # Apply borders to the first two rows except the header row
    row_border = Border(top=Side(border_style="thin", color="000000"),
                        left=Side(border_style="thin", color="000000"),
                        right=Side(border_style="thin", color="000000"),
                        bottom=Side(border_style="thin", color="000000"))

    for row in sheet.iter_rows(min_row=2, max_row=3):
        for cell in row:
            cell.border = row_border

    # Save the Excel file
    workbook.save(file_path)


def create_excel_sheet_for_testcase(file_path):
    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set the sheet name as "Object_repo"
    sheet.title = "FMS_Login"

    # Headers for the Excel sheet
    headers = ['Test_Case', 'User_Story_Tcno', 'Test_Steps', 'Test_data', 'Seq|Object_Repo_Ref|Action',
               'Action Description', 'Results Validation[Automation]', 'Expected_Results[Manual]', 'RunType', 'Case',
               'Depend', 'IncidentIds']

    # Set header values in the first row
    sheet.append(headers)

    # Apply formatting to the header row (underline, bold font, white text color, and red background)
    header_font = Font(bold=True, color="FFFFFF", underline="single")
    header_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

    for cell in sheet[1]:
        cell.font = header_font
        cell.fill = header_fill

    # Apply borders to the first two rows except the header row
    row_border = Border(top=Side(border_style="thin", color="000000"),
                        left=Side(border_style="thin", color="000000"),
                        right=Side(border_style="thin", color="000000"),
                        bottom=Side(border_style="thin", color="000000"))

    for row in sheet.iter_rows(min_row=2, max_row=3):
        for cell in row:
            cell.border = row_border

    # Save the Excel file
    workbook.save(file_path)


test_web_sample = """import os
import cdxg
import configparser
from cdxg import file_data
from wfs.utils.action_test_item import get_tags
from wfs.pages.object_repo_page import object_repox
from cdxg.logging import log
from wfs.utils.common import Create_New_Report, get_results, getdepend, get_line_dict

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "conf.ini")
config = configparser.ConfigParser()
config.read(data_file_path)
test_case_data = config.get("Xldata", "test_case_data")
test_data_json = config.get("Xldata", "test_data_json")
test_object_repo = config.get('Xldata', 'test_object_repo')
test_tags = config.get("Tags", "run_type")
base_url = config.get("Url", "base_url")
xreport = config.get("Xldata", "test_report")
reportpath = Create_New_Report(report=xreport)


line = 7
end_line = 10


class Test_Web_FMS_Login(cdxg.TestCase):

	def start(self):
		self.lpage = object_repox(self.driver)
		self.baseUrl = f'{base_url}'

	@file_data(test_case_data, line=line, end_line=end_line, sheet="FMS_Login")
	def test_oneFMS_Login(self, testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, rtype,
							case, depend, incidentids):
		""""""
		if get_tags(rtype):
			log.info("Test_Tags: " + str(get_tags(rtype)))
		features = "FMS_Login"
		self.maxDiff = None

		if rtype != "skip" and rtype == get_tags(rtype) and rtype is not None:
			dependdata = testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend
			gtres = getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, self.baseUrl, self.driver, ptname=None)
			for xgres in gtres:
				if 'Error' in xgres or gtres == 'Y' or xgres == 'Y':
					get_results(reportpath, features, ustory, testcase, teststeps, testdata, xgres, 
										exresults, gtres, results='FAILED', fontx='FC2C03', sshots=features, incidentids=incidentids)
					self.xFail(gtres)
					break
				if xgres.endswith('YES'):
					if '>>' in str(aresults) and not str(aresults).startswith('>>'):
						aresults = get_line_dict(ptname=None, dname=aresults)
					acresults = str(xgres)+'>>'+str(aresults)
					get_results(reportpath, features, ustory, testcase, teststeps, testdata, acresults, 
										exresults, gtres, results='PASSED', fontx='35FC03', sshots=None, incidentids=incidentids)
					break
		else:
			get_results(reportpath, features, ustory, testcase, teststeps, testdata, 'Testcase Skipped', 
												exresults, results='SKIPPED', fontx='F4D25A', sshots=None, incidentids=incidentids)
			if rtype == "skip":
				self.xSkip(testcase + ": Testcase Skipped, Due to not much information")
			else:
				self.skipTest(reason="Test execution based on Tags :" + str(test_tags) + ": Excludes the rest")
"""

test_zigapp_sample = """import os
import cdxg
import configparser
from cdxg import file_data
from wfs.utils.action_test_item import get_tags
from cdxg.logging import log
from wfs.utils.common import Create_New_Report, get_results, getdepend

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "conf.ini")
config = configparser.ConfigParser()
config.read(data_file_path)
test_case_data = config.get("MobileHost", "test_case_data")
test_data_json = config.get("MobileHost", "test_data_json")
test_object_repo = config.get('MobileHost', 'test_object_repo')
test_tags = config.get("Tags", "run_type")
xreport = config.get("MobileHost", "test_report")
reportpath = Create_New_Report(report=xreport)


line = 2
end_line = None


class Test_Mobile_APP_Login(cdxg.TestCase):

	@file_data(test_case_data, line=line, end_line=end_line, sheet="APP_Login")
	def test_zigAPP_Login(self, testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, rtype,
							case, depend, incidentids):
		""""""
		if get_tags(rtype):
			log.info("Test_Tags: " + str(get_tags(rtype)))
		features = "APP_Login"
		self.maxDiff = None

		if rtype != "skip" and rtype == get_tags(rtype) and rtype is not None:
			dependdata = testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend
			gtres = getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, url=None, driver=None, ptname="Android")
			if 'Error' in gtres or gtres == 'Y':
				get_results(reportpath, features, ustory, testcase, teststeps, testdata, str(gtres), 
										exresults, results='FAILED', fontx='FC2C03', sshots=features, incidentids=incidentids)
				self.xFail(gtres)
			if gtres == 'YES':
				get_results(reportpath, features, ustory, testcase, teststeps, testdata, aresults, 
										exresults, results='PASSED', fontx='35FC03', sshots=None, incidentids=incidentids)
		else:
			get_results(reportpath, features, ustory, testcase, teststeps, testdata, 'Testcase Skipped', 
												exresults, results='SKIPPED', fontx='F4D25A', sshots=None, incidentids=incidentids)
			if rtype == "skip":
				self.xSkip(testcase + ": Testcase Skipped, Due to not much information")
			else:
				self.skipTest(reason="Test execution based on Tags :" + str(test_tags) + ": Excludes the rest")
"""

run_test = """import platform
from cdxg.logging import log
import cdxg
import subprocess
import argparse
from configparser import ConfigParser
from selenium.webdriver import ChromeOptions
from pathlib import Path

mypath = Path.cwd()
cObject = ConfigParser()
cObject.read('conf.ini')

from wfs.utils.action_test_item import *

if __name__ == '__main__':
    # run test file
    parser = argparse.ArgumentParser(description='Add Arguments')
    parser.add_argument("--t", help="Add run type Tags")
    parser.add_argument("--b", help="Add Browser/App")
    parser.add_argument("--s", help="Give Sheetname")
    parser.add_argument("--l", help="Give Executelines")
    args = parser.parse_args()
    tags_add = cObject['Tags']
    tags_add['run_type'] = args.t
    with open('conf.ini', 'w') as cf:
        cObject.write(cf)

    sheetname = args.s
    exeLine = args.l

    if args.b == 'gc':
        subprocess.Popen(['mitmdump', '-s', 'proxy.py']) # , '--web-port', '8081'])
        log.info('MitmDump and Proxy Connection Started......')
        time.sleep(1)
        proxy_address = "127.0.0.1:8080"
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={proxy_address}')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        # chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPad Pro"})
        browser = {
            "browser": args.b,
            "options": chrome_options,
        }
    else:
        browser = args.b

    if args.b in ['Android', 'iOS']:
        fpath = mypath / "test_data" / "mobile" / "get_text_item.txt"
        with open(fpath, 'r+') as file:
            file.truncate(0)
        test_case_data = cObject.get('MobileHost', 'test_case_data')
        test_pfix = cObject.get('MobileHost', 'test_prefix')
        generate_test_object_repo(test_case_data, pfix=test_pfix, dx='Mobile', ptname=args.b, sheetname=sheetname,
                                  exeLine=exeLine)
        description = 'App : ' + args.b + ' / RunType : ' + cObject.get('Tags', 'run_type')
        cdxg.main("./test_dir/test_zigapp.py", tester='Saa Saa', description=description,
                    title='Fleet Management Services[oneFMS]', report='result.html')
        file_pathxx = "./test_data/mobile/get_text_item.txt"
    else:
        fpath = mypath / "test_data" / "web" / "get_text_item.txt"
        with open(fpath, 'r+') as file:
            file.truncate(0)
        test_case_data = cObject.get('Xldata', 'test_case_data')
        test_pfix = cObject.get('Xldata', 'test_prefix')
        generate_test_object_repo(test_case_data, pfix=test_pfix, sheetname=sheetname, exeLine=exeLine)
        description = 'Browser : ' + args.b + ' / RunType : ' + cObject.get('Tags', 'run_type')
        cdxg.main("./test_dir/test_onefms.py", browser=browser, tester='Saa Saa', description=description,
                    title='Fleet Management Services[oneFMS]', report='result.html')
    if args.b == 'gc':
        system = platform.system()
        if system == 'Windows':
            subprocess.Popen(['taskkill', '/F', '/IM', 'mitmdump'])
        else:
            subprocess.Popen(['kill', '-f', 'mitmdump'])
        log.info('MitmDump and proxy Connection Closed......')
"""

test_wproxy = """from mitmproxy import ctx
from mitmproxy.addonmanager import AddonManager
from mitmproxy import http
from mitmproxy.tools.main import mitmproxy
from pathlib import Path
import os, json
import platform

mypath = Path.cwd()


def getspliter(apix, method):
    spltapi = apix.split('/v1.0/')[1]
    if '/' in spltapi and '?' not in spltapi:
        spltapi = str(spltapi).replace('/', '_')
    if '?' in spltapi:
        spltapi = str(spltapi).split('?')[0]
    return spltapi + '_' + method.lower()


class APIEndpointLogger:
    def __init__(self):
        self.api_endpoints = set()

    def request(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.path.startswith("/fms/api/v1.0/"):
                print("API Request:" + str(flow.request.path))
                # Save the request content to a file
                fnamex = getspliter(apix=flow.request.path, method=flow.request.method)
                request_filename = mypath / 'test_data' / 'web' / 'pxy' / 'request'
                os.makedirs(request_filename, exist_ok=True)
                request_filename = str(request_filename / (fnamex + '.json'))
                getrequest = json.loads(flow.request.content.decode())
                with open(request_filename, 'w') as file:
                    # file.write(json.dump(getrequest))
                    json.dump(getrequest, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            return

    def response(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.path.startswith("/fms/api/v1.0/"):
                self.api_endpoints.add((flow.request.path, flow.response.content))
                fnamex = getspliter(apix=flow.request.path, method=flow.request.method)
                response_filename = mypath / 'test_data' / 'web' / 'pxy' / 'response'
                os.makedirs(response_filename, exist_ok=True)
                response_filename = str(response_filename / (fnamex + '.json'))
                getresponse = json.loads(flow.response.content.decode())
                with open(response_filename, 'w') as file:
                    # file.write(json.dump(getresponse))
                    json.dump(getresponse, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            return


def done(self) -> None:
    print("API Endpoints:")
    for endpoint in self.api_endpoints:
        print(f"Path: {endpoint[0]}")
        print(f"Content: {endpoint[1]}")
        print("-" * 20)


addons = [
    APIEndpointLogger()
]


def start_proxy():
    mitmproxy(["-s", __file__])


if __name__ == "__main__":
    start_proxy()
"""

test_mproxy = """from mitmproxy import ctx
from mitmproxy.addonmanager import AddonManager
from mitmproxy import http
from mitmproxy.tools.main import mitmproxy
from pathlib import Path
import os, json
import platform

mypath = Path.cwd()


# https://interapps-uat.cdgtaxi.com.sg
def getspliter(apix, method):
    spltapi = apix.split('/dcp-cms/rest/')[1]
    if '/' in spltapi and '?' not in spltapi:
        spltapi = str(spltapi).replace('/', '_')
    if '?' in spltapi:
        spltapi = str(spltapi).split('?')[0]
    return spltapi + '_' + method.lower()


class APIEndpointLogger:
    def __init__(self):
        self.api_endpoints = set()

    def request(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.path.startswith("/dcp-cms/rest/"):
                print("API Request:" + str(flow.request.path))
                # Save the request content to a file
                fnamex = getspliter(apix=flow.request.path, method=flow.request.method)
                request_filename = mypath / 'test_data' / 'mobile' / 'pxy' / 'request'
                os.makedirs(request_filename, exist_ok=True)
                request_filename = str(request_filename / (fnamex + '.json'))
                getrequest = json.loads(flow.request.content.decode())
                with open(request_filename, 'w') as file:
                    # file.write(json.dump(getrequest))
                    json.dump(getrequest, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            return

    def response(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.path.startswith("/dcp-cms/rest/"):
                self.api_endpoints.add((flow.request.path, flow.response.content))
                fnamex = getspliter(apix=flow.request.path, method=flow.request.method)
                response_filename = mypath / 'test_data' / 'mobile' / 'pxy' / 'response'
                os.makedirs(response_filename, exist_ok=True)
                response_filename = str(response_filename / (fnamex + '.json'))
                getresponse = json.loads(flow.response.content.decode())
                with open(response_filename, 'w') as file:
                    # file.write(json.dump(getresponse))
                    json.dump(getresponse, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            return


def done(self) -> None:
    print("API Endpoints:")
    for endpoint in self.api_endpoints:
        print(f"Path: {endpoint[0]}")
        print(f"Content: {endpoint[1]}")
        print("-" * 20)


addons = [
    APIEndpointLogger()
]


def start_proxy():
    mitmproxy(["-s", __file__])


if __name__ == "__main__":
    start_proxy()
"""

conf_requires = """[Url]
base_url = https://onefms-uat.zig.live/

[Xldata]
test_case_data = test_data/web/fms_test_case_and_data.xlsx
test_object_repo = test_data/web/fms_object_repo.xlsx
test_data_json = test_data/web/test_data_repo.txt
test_obj_sheet1 = Object_Repo_BasePage
test_obj_col1 = BasePage
test_prefix = FMS_
test_report = FMS_Report

[Tags]
run_type = Smoke

[MobileHost]
test_case_data = test_data/mobile/app_test_case_and_data.xlsx
test_object_repo = test_data/mobile/app_object_repo.xlsx
test_data_json = test_data/mobile/test_data_repo.txt
test_prefix = APP_
test_report = APP_Report
local_host = http://localhost:4723/wd/hub
android_current_device_pax = emulator-5554
android_current_device_drv = emulator-5556
android_app_path_pax = ShopFront.apk
android_app_path_driver = Driverapp.apk
android_activity_pax = com.codigo.comfort
android_activity_drv = com.codigo.cdgdriver.uat
android_platform_version = 10
ios_app_path_pax = ShopFront.ipa
ios_app_path_driver = Driverapp.ipa
ios_activity = 
ios_current_device = iphone 13
ios_platform_version = 15.6
ios_activity_pax = com.codigo.comfort
ios_activity_drv = com.codigo.cdgdriver.uat
"""

test_requires = """asyncio
ffmpeg-python
"""