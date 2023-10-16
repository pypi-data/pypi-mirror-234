import configparser
import os
import random
import string
import xlrd
import ffmpeg
from wfs.utils.parseexcel import ParseExcel
from wfs.pages.base_page import *
from wfs.pages.app_page import *
from wfs.utils.common import get_line_dict
from pathlib import Path

mypath = Path.cwd()
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = mypath / "conf.ini"
config = configparser.ConfigParser()
# config.read(data_file_path)
# test_tags = config.get('Tags', 'run_type')


def get_test_action_data(steps_line, testdata, action, actiondesc):
    testdata = testdata.split('\n')
    testxdata = testdata[steps_line]

    actiondata = action.split('\n')
    actionxdata = actiondata[steps_line].split('|')

    actiondesc = actiondesc.split('\n')
    actionxdesc = actiondesc[steps_line]
    return testxdata, actionxdata[0], actionxdata[1], actionxdata[2], actionxdesc


def readlastine(filepath):
    with open(filepath, 'r') as f:
        last_linex = f.readlines()
        if len(last_linex) == 1:
            last_line = last_linex[0]
        elif len(last_linex) > 1:
            last_line = last_linex[-1]
        else:
            last_line = 'NA'
    return last_line


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_object_repo(test_object_repo, test_generate):
    getallxm = ParseExcel(test_object_repo).get_all_rows_columns_data()
    # log.info('Fetch all Generate Object repo: ' + str(getallxm))
    with open(test_generate, 'w') as f:
        f.write('from poium import Page, Element, Elements\n\n\n')
        f.write('class Object_Repo_Page(Page):\n\n')
        for getxl in getallxm:
            if getxl['BasePage'] is not None and getxl['BasePage'] != 'BasePage':
                if getxl['FetchElements'] == 'M':
                    felements = 'Elements'
                else:
                    felements = 'Element'
                f.write(
                    '\telement_' + getxl['Description'] + ' = ' + str(felements) + '(' + getxl['Locators'] + '="' +
                    getxl['Elements'] + '", describe="' + getxl['Description'] + '")\n')
        f.close()


def delete_line_with_word(file_name, word):
    """Delete lines from a file that contains a given word / sub-string """
    delete_line_by_condition(file_name, lambda x: word in x)


def delete_line_by_condition(original_file, condition):
    """ In a file, delete the lines at line number in given list"""
    dummy_file = original_file + '.bak'
    is_skipped = False
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            # if current line matches the given condition then skip that line
            if condition(line) == False:
                write_obj.write(line)
            else:
                is_skipped = True
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)


def getData(xlFilename, sheetname):
    data = []
    wbook = xlrd.open_workbook(xlFilename)
    sheet = wbook.sheet_by_name(sheetname)
    for i in range(1, sheet.nrows):
        data.append([sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3),
                     sheet.cell_value(i, 4), sheet.cell_value(i, 5), sheet.cell_value(i, 6), sheet.cell_value(i, 7),
                     sheet.cell_value(i, 8), sheet.cell_value(i, 9), sheet.cell_value(i, 10)])
    # print(data)
    return data


def get_all_data(xlfilename, sheetname):
    wbook = ParseExcel(xlfilename)
    sheet = wbook.set_sheet_by_name(sheetname)
    totalrows = sheet.max_row
    totalcols = sheet.max_column
    sheet_data = []

    for rows in sheet.iter_rows():
        row_cells = []
        for cell in rows:
            row_cells.append(cell.value)
        sheet_data.append(row_cells)
    datasheet = []
    for i in range(2, len(sheet_data) + 1):
        datalist = []
        for j in range(1, totalcols + 1):
            data = sheet.cell(row=i, column=j).value
            datalist.insert(j, data)
        # datasheet.append(sheet_data[i][j] + ", " + str(sheet_data[i][j]))
        datasheet.insert(i, datalist)
    return datasheet


def get_tags(rtype='smoke'):
    config.read(data_file_path)
    gettag = config['Tags']
    test_tags = gettag['run_type']
    if rtype is not None:
        rty = rtype.split(',')
        ttags = test_tags.split(',')
        if len(rty) == 1 and len(ttags) >= 1:
            if test_tags.find(rty[0]) != -1:
                t_xgs = None
                for txgs in ttags:
                    if txgs == rty[0]:
                        t_xgs = txgs
                return t_xgs
        else:
            xtype, txn = [], None
            for tgs in ttags:
                for rxt in rty:
                    if rxt == tgs:
                        txn = rxt
                        break
                if txn == tgs:
                    xtype.append('Y')
                else:
                    xtype.append('N')
            if 'Y' in list(set(xtype)):
                return rtype


def get_sheetnames_excel(test_case_data, pfix='FMS_', itemdata='NSH_001_TC01', ustory=None):
    get_excel_data, gtdata = None, []
    getxcl = ParseExcel(test_case_data)
    getallxm = getxcl.get_sheetnames()
    getdata_item = itemdata.split(',')
    getdata_item.append(ustory)
    for gdata in range(0, len(getdata_item)):
        for xallm in getallxm:
            if pfix in xallm:
                get_excel_data = ParseExcel(test_case_data).get_row_all_col_data(sheetname=xallm,
                                                                                 columnname="User_Story_Tcno",
                                                                                 pagename=getdata_item[gdata])
                if get_excel_data:
                    gtdata.append(get_excel_data)
    return gtdata


def getall_actions(testcase, lpage, gAitem, gTestitem, gFelements, linex, gRstring, aresults, exresults, case, gItems,
                   gLocator, gElementor, gAction, gtitems, ptname):
    gready = gLocator, gElementor, gAction, gFelements
    try:
        if str(aresults).startswith('>>'):
            aresults = get_ordering_table(lpage, gAitem, gready, aresults, gTestitem)
            # print(aresults)
        else:
            if '>>' in gTestitem and not str(gTestitem).startswith('>>'):
                gTestitem = get_line_dict(ptname, dname=gTestitem)
            if '>>' in str(aresults) and not str(aresults).startswith('>>'):
                aresults = get_line_dict(ptname, dname=aresults)
            if '*' in aresults:
                aresults = str(aresults).split('*')
                print(aresults)
        gTestitem = getextra(keyitem=gTestitem, ustory=gtitems[2], kword=str(linex).split(':')[0], rstring=gRstring,
                             ptname=ptname)
        global gTx
        if gAitem == 'url':
            gTx = 'Navigated to url ' + config.get('Url', 'base_url')
        elif gAitem == 'xurl':
            gTx = 'Navigated to url ' + lpage.get_current_url()
        elif gAitem == 'type':
            """Type"""
            gTx = get_type_key(lpage=lpage, item=gAitem, keyitem=gTestitem, gready=gready)
        elif gAitem == 'click':
            """Click"""
            gTx = get_click(lpage=lpage, item=gAitem, gready=gready)
        elif gAitem == 'text':
            """Text"""
            gTx = get_text(lpage=lpage, item=gAitem, felement=gFelements, aresults=aresults, case=case,
                           testcase=testcase, exresults=exresults, stepline=linex, gitems=gItems, gready=gready,
                           testitem=gTestitem, ptname=ptname)
        elif gAitem == 'link_text':
            """Link_text"""
            gTx = get_link_text(lpage=lpage, item=gAitem, testitem=gTestitem, felement=gFelements, gready=gready)
        elif gAitem in ['title', 'row', 'asc', 'desc']:
            """Title"""
            gTx = get_page_title(lpage=lpage, item=gAitem, case=case, testcase=testcase,  aresults=aresults,
                                 exresults=exresults, stepline=linex, gready=gready, gtitems=gtitems)
        elif gAitem == 'option':
            """Select"""
            gTx = get_select_item(lpage=lpage, item=gAitem, keyitem=gTestitem, gready=gready)
        elif gAitem in ['attrib']:
            """Get Attributes"""
            gTx = get_dom_attribute(lpage=lpage, item=gAitem, case=case, testcase=testcase,  aresults=aresults,
                                 exresults=exresults, stepline=linex, gready=gready, gtitems=gtitems, testitem=gTestitem)
        elif gAitem == 'keys':
            """Keys"""
            gTx = get_keys_press(lpage=lpage, gready=gready, keyitem=gTestitem)
        elif gAitem in ['hover', 'scroll']:
            """Hover, Scrolls"""
            gTx = mouse_actions(lpage=lpage, item=gAitem, gready=gready)
        elif gAitem in ['idata']:
            gTx = get_common(lpage=lpage, item=gAitem, gready=gready, attriname=gTestitem, aresults=aresults)
        elif gAitem in ['SwipeUp', 'SwipeDn']:
            """Swipe"""
            gTx = get_tap_swipe(lpage=lpage, item=gAitem, ax=None, ay=None)
        elif gAitem in ['atype', 'kshown', 'hkboard', 'home', 'back', 'size']:
            """keyboard activites"""
            gTx = get_key_text(lpage=lpage, item=gAitem, ktext=gTestitem)
        elif gAitem in ['atext', 'aclick']:
            if ptname == "Android":
                """app actions for android"""
                gTx = getAndroid(lpage=lpage, item=gAitem, greadyx=gready, desc=gTestitem)
            if ptname == "iOS":
                """app actions for iOS"""
                gTx = getiOS(lpage=lpage, item=gAitem, greadyx=gready, desc=gTestitem)
        else:
            gTx = gTx
        """Clear stored data"""
        '''if gtitems[5] != 'Y':
            getxxextra(keyitem=gTestitem, ustory=gtitems[2], kword=str(linex).split(':')[0], rstring=gRstring,
                       retnx=gTx, ptname=ptname)'''
        gstp = str(linex).split(':')[0]
        gTx = gstp + ':' + gTx
        # delete_line_with_word(test_data_json, gRstring)
        return gTx
    except Exception as e:
        print(traceback.print_exc())
        return 'Error : ' + str(e)


def generate_test_object_repo(test_case_data, pfix='FMS_', dx=None, ptname=None, sheetname=None, exeLine=None):
    sLine, eLine = 2, None
    getxcl = ParseExcel(test_case_data)
    getallxm = getxcl.get_sheetnames()
    getxmall = []
    if sheetname:
        for y in eval(sheetname):
            for x in range(0, len(getallxm)):
                if x == y or getallxm[x] == y:
                    getxmall.append(getallxm[x])
                    break
        getallxm = getxmall
    if exeLine:
        if ',' in exeLine:
            sLine, eLine = str(exeLine).split(',')
        else:
            sLine, eLine = exeLine, None
    if dx:
        pathdata_file = mypath / 'test_dir' / 'test_zigapp.py'
    else:
        pathdata_file = mypath / 'test_dir' / 'test_onefms.py'
    with open(pathdata_file, 'w') as f:
        f.write('import os\n')
        f.write('import cdxg\n')
        f.write('import configparser\n')
        f.write('from cdxg import file_data\n')

        # f.write('from wfs.pages.action_step import get_test_steps\n')
        f.write('from wfs.utils.action_test_item import get_tags\n')
        if dx is None:
            f.write('from wfs.pages.object_repo_page import object_repox\n')
        f.write('from cdxg.logging import log\n')
        f.write('from wfs.utils.common import Create_New_Report, get_results, getdepend, get_line_dict\n\n')
        # if dx:
        #    f.write('from confapp import pax_session, drv_session\n\n')

        f.write('BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))\n')
        f.write('data_file_path = os.path.join(BASE_PATH, "conf.ini")\n')
        f.write('config = configparser.ConfigParser()\n')
        f.write('config.read(data_file_path)\n')
        if dx:
            f.write('test_case_data = config.get("MobileHost", "test_case_data")\n')
            f.write('test_data_json = config.get("MobileHost", "test_data_json")\n')
            f.write("test_object_repo = config.get('MobileHost', 'test_object_repo')\n")
        else:
            f.write('test_case_data = config.get("Xldata", "test_case_data")\n')
            f.write('test_data_json = config.get("Xldata", "test_data_json")\n')
            f.write("test_object_repo = config.get('Xldata', 'test_object_repo')\n")
        f.write('test_tags = config.get("Tags", "run_type")\n')
        if dx:
            f.write('xreport = config.get("MobileHost", "test_report")\n')
            twx = 'Mobile'
        else:
            f.write('base_url = config.get("Url", "base_url")\n')
            f.write('xreport = config.get("Xldata", "test_report")\n')
            twx = 'Web'
        f.write('reportpath = Create_New_Report(report=xreport)\n\n\n')
        f.write('line = ' + str(sLine) + '\n')
        f.write('end_line = ' + str(eLine) + '\n\n\n')

        for getxl in getallxm:
            if pfix in getxl:
                f.write('class Test_' + str(twx) + '_' + str(getxl) + '(cdxg.TestCase):\n\n')
                if dx is None:
                    f.write('\tdef start(self):\n')
                    f.write('\t\tself.lpage = object_repox(self.driver)\n')
                    f.write("\t\tself.baseUrl = f'{base_url}'\n\n")

                    appx = 'one'
                else:
                    appx = 'zig'

                f.write('\t@file_data(test_case_data, line=line, end_line=end_line, sheet="' + str(getxl) + '")\n')
                f.write(
                    '\tdef test_' + str(appx) + str(
                        getxl) + '(self, testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, rtype,\n')
                f.write('\t\t\t\t\t\t\tcase, depend, incidentids):\n')
                f.write('\t\t""""""\n')
                f.write('\t\tif rtype and case is not None:\n')
                f.write('\t\t\txtype = rtype + "," + case\n')
                f.write('\t\telse:\n')
                f.write('\t\t\txtype = rtype if case is None else case\n')
                f.write('\t\tif get_tags(xtype):\n')
                f.write('\t\t\tlog.info("TestCase : " + str(ustory) + "-" + str(testcase))\n')
                f.write('\t\t\tlog.info("Test_Tags : " + str(get_tags(xtype)))\n\n')
                f.write('\t\tfeatures = "' + str(getxl) + '"\n')
                f.write("\t\tself.maxDiff = None\n")
                f.write('\t\tif "skip" not in xtype and xtype == get_tags(xtype) and xtype is not None:\n')
                f.write(
                    '\t\t\tdependdata = testcase, ustory, teststeps, testdata, action, adescribe, aresults, exresults, case, depend\n')
                if dx is None and ptname is None:
                    f.write(
                        '\t\t\tgtres = getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, self.baseUrl, self.driver, ptname=None)\n')
                else:
                    f.write(
                        '\t\t\tgtres = getdepend(test_case_data, reportpath, features, test_object_repo, test_data_json, dependdata, url=None, driver=None, ptname="' + str(
                            ptname) + '")\n')
                # f.write("\t\t\tprint(gtres)\n")
                f.write("\t\t\tfor xgres in gtres:\n")
                f.write("\t\t\t\tif 'Error' in xgres or gtres == 'Y' or xgres == 'Y':\n")
                f.write(
                    "\t\t\t\t\tget_results(reportpath, features, ustory, testcase, teststeps, testdata, xgres, \n")
                f.write(
                    "\t\t\t\t\t\t\t\t\t\texresults, gtres, results='FAILED', fontx='FC2C03', sshots=features, incidentids=incidentids)\n")
                f.write('\t\t\t\t\tself.xFail(gtres)\n')
                f.write('\t\t\t\t\tbreak\n')
                f.write("\t\t\t\tif xgres.endswith('YES'):\n")
                f.write("\t\t\t\t\tif '>>' in str(aresults) and not str(aresults).startswith('>>'):\n")
                f.write("\t\t\t\t\t\taresults = get_line_dict(ptname=" + str(ptname) + ", dname=aresults)\n")
                f.write("\t\t\t\t\tacresults = str(xgres)+'>>'+str(aresults)\n")
                f.write(
                    "\t\t\t\t\tget_results(reportpath, features, ustory, testcase, teststeps, testdata, acresults, \n")
                f.write(
                    "\t\t\t\t\t\t\t\t\t\texresults, gtres, results='PASSED', fontx='35FC03', sshots=None, incidentids=incidentids)\n")
                f.write('\t\t\t\t\tbreak\n')
                f.write('\t\telse:\n')
                f.write('\t\t\tif rtype == "skip":\n')
                f.write('\t\t\t\tself.xSkip(testcase + ": Testcase Skipped, Due to not much information")\n')
                f.write(
                    "\t\t\t\tget_results(reportpath, features, ustory, testcase, teststeps, testdata, 'Testcase Skipped', \n")
                f.write(
                    "\t\t\t\t\t\t\t\t\t\t\t\texresults, results='SKIPPED', fontx='F4D25A', sshots=None, incidentids=incidentids)\n")
                f.write('\t\t\telse:\n')
                f.write(
                    '\t\t\t\tself.skipTest(reason="Test execution based on Tags :" + str(test_tags) + ": Excludes the rest")\n')
                f.write('\n\n')
    f.close()


def mixedcharacters(k=5):
    mixed_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return mixed_chars


def getextra(keyitem, ustory, kword, rstring, ptname):
    if '*.*' in keyitem:
        keyitem = str(keyitem).replace('*.*', '_' + str(mixedcharacters()))
    ptn = 'web'
    if ptname:
        ptn = 'mobile'
    with open(mypath / 'test_data' / ptn / 'get_text_item.txt', 'a+') as ftxt:
        ftxt.write(ustory + '|' + keyitem + '|' + kword + '|' + rstring + '|\n')
    return keyitem


def getxxextra(keyitem, ustory, kword, rstring, retnx, ptname):
    ptn = 'web'
    if ptname:
        ptn = 'mobile'
    with open(mypath / 'test_data' / ptn / 'text_data_repo.txt', 'a+') as ftxt:
        ftxt.write(ustory + '|' + keyitem + '|' + kword + '|' + rstring + '|' + retnx + '|\n')
    return keyitem


def getmultipleKeys(keyitem):
    getlen = []
    if ',' in keyitem:
        getsplit = str(keyitem).split(',')
        for xlen in getsplit:
            getlen.append(getextra(xlen))
    else:
        getlen.append(keyitem)
    return getlen


def capture_frame(driver, output_file):
    # Capture the screenshot using Selenium
    screenshot = driver.get_screenshot_as_png()

    # Save the screenshot to a file
    with open(output_file, 'wb') as file:
        file.write(screenshot)


def start_video_recording(driver):
    # Start video recording using ffmpeg
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_video_file = mypath / 'reports' / "videos" / f"scenario_{timestamp}.mp4"
    # Set the output video file path
    # output_video_file = 'output.mp4'

    # Start recording frames
    ffmpeg_process = (
        ffmpeg
        .input('pipe:', format='png', framerate=30)
        .output(output_video_file, pix_fmt='yuv420p')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

    # Capture frames at regular intervals
    for frame_number in range(300):  # Capture 300 frames
        capture_frame(driver, 'frame{:03d}.png'.format(frame_number))
    return ffmpeg_process


def stop_video_recording(ffmpeg_process):
    # Stop video recording
    # Close the ffmpeg process
    ffmpeg_process.stdin.write("q")
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
