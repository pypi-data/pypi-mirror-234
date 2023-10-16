import shutil
import pyautogui
import time
from pathlib import Path
from cdxg.appium_lab import AppiumLab
from cdxg import Steps
from wfs.pages.action_step import get_test_steps
from wfs.pages.object_repo_page import object_repox
from wfs.utils.parseexcel import ParseExcel
from wfs.utils.confapp import pax_session, drv_session
from configparser import ConfigParser

mypath = Path.cwd()  # .parent
cObject = ConfigParser()
cObject.read('conf.ini')


def get_results(xlcreate, features, userstory, testcase, teststeps, testdata, actResults, expResults, aresults, results,
                fontx,
                sshots, incidentids, comments='{Step1: Go to Url, Step2: Yes}'):
    global screens
    reportpath = ParseExcel(excel_path=xlcreate)
    reportpath.set_sheet_by_name('Web_Results')
    get_total_rows = reportpath.get_max_row_no()
    aresults = '\n'.join(aresults)
    try:
        reportpath.write_cell_content_colored(get_total_rows + 1, 1, get_total_rows - 2)
        reportpath.write_cell_content_colored(get_total_rows + 1, 2, features)
        reportpath.write_cell_content_colored(get_total_rows + 1, 3, userstory)
        reportpath.write_cell_content_colored(get_total_rows + 1, 4, testcase)
        reportpath.write_cell_content_colored(get_total_rows + 1, 5, teststeps)
        reportpath.write_cell_content_colored(get_total_rows + 1, 6, testdata)
        reportpath.write_cell_content_colored(get_total_rows + 1, 7, str(aresults))
        reportpath.getcomment(get_total_rows + 1, 7, str(actResults))
        reportpath.write_cell_content_colored(get_total_rows + 1, 8, str(expResults))
        if results == 'PASSED':
            reportpath.write_cell_content_colored(get_total_rows + 1, 9, '✅', font=fontx)
        elif results == 'SKIPPED':
            reportpath.write_cell_content_colored(get_total_rows + 1, 9, '⚠️', font=fontx)
        else:
            reportpath.write_cell_content_colored(get_total_rows + 1, 9, '❌', font=fontx)
        # reportpath.write_cell_content_colored(get_total_rows + 1, 9, results, font=fontx)
        if results == 'FAILED':
            screens = lpage.screen_shots(screenshot_path=str(sshots + '_' + str(get_total_rows + 1)))
            reportpath.sHyperlink(get_total_rows + 1, 10, sshot=sshots + '_' + str(get_total_rows + 1),
                                  sshotpath=str(screens))
        else:
            reportpath.write_cell_content_colored(get_total_rows + 1, 10, sshots)
        reportpath.write_cell_content_colored(get_total_rows + 1, 11, incidentids)
    except Exception as e:
        if ValueError:
            for xna in actResults:
                reportpath.write_cell_content_colored(get_total_rows + 1, 7, xna)
        print(str(e))


def Create_New_Report(report):
    otime = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    reportfolderpath = report + "_" + otime + ".xlsx"
    shutil.copy(mypath / 'reports' / 'web_results.xlsx', mypath / 'reports' / reportfolderpath)
    return mypath / 'reports' / reportfolderpath


def screenshots(sname):
    screenshot = pyautogui.screenshot()
    snamex = mypath / 'reports' / 'screenshots' / sname
    screenshot.save(snamex)
    return snamex


def getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, url, driver, ptname):
    from wfs.utils.action_test_item import getall_actions, get_sheetnames_excel
    testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend = dependdata
    gtres = None

    def execute_steps(testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend):
        gtresx = []
        linex = teststeps.split("\n")
        descp = adescribe.split("\n")
        tdatax = testdata.split("\n")
        # arets = aresults.split("\n")
        for steps_line in range(0, len(linex)):
            Steps(desc=ustory + ":" + linex[steps_line])
            getallx = get_test_steps(test_object_repo, test_data_json, tstepx=linex[steps_line], steps_line=steps_line,
                                     testdata=str(testdata),
                                     action=str(action), actiondesc=str(adescribe), ptname=ptname)

            def getExe(get_all):
                global lpage, ddriver, paxdriver, drvdriver
                gLocator, gElementor, gAction, gDescribe, gStepline, gAitem, gTestitem, gFelements, gItems, gRstring = get_all
                if ptname:

                    if '[Pax]' in gStepline or '[P]' in gStepline:
                        try:
                            if '[P]' in gStepline:
                                paxdriver.activate_app(app_id=cObject.get('MobileHost', str(ptname) + '_activity_pax'))
                                # paxdriver.activate_app(app_id='com.codigo.comfort')
                            else:
                                # drvdriver.background_app(-1)
                                paxdriver = pax_session(ptname, False)
                        except Exception as e:
                            paxdriver = pax_session(ptname, False)

                    if '[Drv]' in gStepline or '[D]' in gStepline:
                        try:
                            if '[D]' in gStepline:
                                drvdriver.activate_app(app_id=cObject.get('MobileHost', str(ptname) + '_activity_drv'))
                                # drvdriver.activate_app(app_id='com.codigo.cdgdriver.uat')
                            else:
                                paxdriver.background_app(-1)
                                drvdriver = drv_session(ptname, False)
                        except Exception as e:
                            drvdriver = drv_session(ptname, False)

                    if '[Pax]' in gStepline or '[P]' in gStepline:
                        lpage = object_repox(paxdriver)

                    if '[Drv]' in gStepline or '[D]' in gStepline:
                        lpage = object_repox(drvdriver)
                else:
                    if gAitem in ["url", "xurl"]:
                        if gTestitem == '***':
                            gTestitem = ''
                        driver.get(url + gTestitem)
                        driver.maximize_window()
                        lpage = object_repox(driver)

                gtitems = reportpath, features, ustory, teststeps, testdata, depend, tdatax[
                    steps_line]  # , arets[steps_line]
                if ',' in gAction:
                    gactionItems = str(gAction).split(',')
                    if gAitem in gactionItems: gAction = gAitem
                gtresults = getall_actions(testcase, lpage, gAitem, gTestitem, gFelements, linex[steps_line], gRstring,
                                           aresults, exresults, case, gItems, gLocator, gElementor, gAction, gtitems,
                                           ptname)
                return gtresults

            if getallx is not None and 'Error' not in getallx:
                for xx in range(len(getallx)):
                    get_all = getallx[xx].split("|")
                    astx = getExe(get_all)
                    gtresx.append(astx)
                    if 'Error' in gtresx and gtresx is not None:
                        break
            else:
                gtresx.append(getallx)
        return gtresx

    if depend is not None:
        gtdata = get_sheetnames_excel(test_case_data, pfix="FMS_", itemdata=depend, ustory=ustory)
        for xlen in range(0, len(gtdata)):
            testcase = gtdata[xlen][0]["Test_Case"]
            ustory = gtdata[xlen][0]["User_Story_Tcno"]
            teststeps = gtdata[xlen][0]["Test_Steps"]
            testdata = gtdata[xlen][0]["Test_data"]
            action = gtdata[xlen][0]["Seq|Object_Repo_Ref|Action"]
            adescribe = gtdata[xlen][0]["Action Description"]
            aresults = gtdata[xlen][0]["Results Validation[Automation]"]
            exresults = gtdata[xlen][0]["Expected_Results[Manual]"]
            case = gtdata[xlen][0]["Priority"]
            depend = gtdata[xlen][0]["Depend"]
            if depend is None:
                depend = 'Y'
            gtres = execute_steps(testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case,
                                  depend)
    else:
        gtres = execute_steps(testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case,
                              depend)
    print('Results : ' + str(gtres))
    return gtres


def get_line_dict(ptname, dname):
    ptn = 'web'
    if ptname:
        ptn = 'mobile'
    with open(mypath / 'test_data' / ptn / 'get_text_item.txt', 'r') as frd:
        lines = frd.readlines()
    data = lines
    # print(data)

    result = {}

    for item in data:
        parts = item.strip().split('|')
        if len(parts) == 5:
            if parts[2] != '***':
                result.setdefault(parts[0], {})[parts[2]] = parts[1]
    # print(result)
    result = {k: {key: value for key, value in v.items() if value != '***'} for k, v in result.items() if v}

    if all(char in dname for char in (',', '>>')):
        yall = []
        getxall = dname.split(',')
        for xall in getxall:
            if '>>' in xall:
                dxt, nmxt = xall.split('>>')
                yall.append(result[dxt][nmxt])
            else:
                yall.append(xall)
    else:
        dxt, nmxt = dname.split('>>')
        yall = result[dxt][nmxt]
    return yall


def get_expected(keyitem):
    getlen = []
    if '*' in keyitem:
        getsplit = str(keyitem).split('*')
        for xlen in getsplit:
            getlen.append(xlen)
    else:
        getlen = keyitem  # .append(keyitem)
    return getlen


def get_check_list(gtx, artx):
    itm = []
    mitm = []
    gtx_items = gtx
    if type(gtx) is not list:
        gtx_items = gtx.split(',')
    no_data_available = True
    alldata = 'Y'
    for item in gtx_items:
        if item not in artx:
            alldata = 'N'
            mitm.append(item)
            no_data_available = False
    if no_data_available:
        alldata = alldata
        mitm = 'Y'
    itm.append(alldata)
    return itm, gtx_items, mitm


def getcheckorder(order_list, expected_order):
    result = None
    if type(expected_order) is not list:
        if ',' in expected_order and '<<' not in expected_order:
            expected_order = expected_order.split(',')

            def check_order(order_list, expected_order):
                pn = []
                exp = 0
                for xorder in order_list:
                    try:
                        if xorder == expected_order[exp]:
                            exp = exp
                            pn.append('Y')
                        elif xorder != expected_order[exp]:
                            exp += 1
                            if xorder == expected_order[exp]:
                                exp = exp
                                pn.append('Y')
                            else:
                                pn.append('N')
                        else:
                            exp += 1
                            pn.append('N')
                    except Exception:
                        pn.append('N')
                for yorder in expected_order:
                    if yorder not in order_list:
                        pn.append('N')
                return list(set(pn)), expected_order, None

            result = check_order(order_list, expected_order)
        else:
            if '<<' in expected_order:
                expected_order = expected_order.split('<<')[1]
            result = get_check_list(gtx=expected_order, artx=order_list)
    else:
        result = get_check_list(gtx=expected_order, artx=order_list)
    return result
