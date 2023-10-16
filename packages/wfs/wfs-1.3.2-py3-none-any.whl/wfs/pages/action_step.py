from wfs.utils.parseexcel import ParseExcel


def get_test_steps(test_object_repo, test_data_json, tstepx, steps_line, testdata, action, actiondesc, ptname):
    from wfs.utils.action_test_item import get_test_action_data, id_generator
    try:
        data = None
        # jsonfile = open(test_data_json, 'w+')
        test_data_item, action_no, action_page_item, action_item, actionxdesc = get_test_action_data(steps_line,
                                                                                                     testdata,
                                                                                                     action, actiondesc)
        get_excel_data = ParseExcel(test_object_repo).get_row_all_col_data(sheetname="Object_Repo_BasePage",
                                                                           columnname="BasePage",
                                                                           pagename=action_page_item)
        # print(get_excel_data)
        getdescp = get_action_description(get_excel_data, actionxdesc, ptname)
        # print(getdescp)

        data = []
        if test_data_item != "***" and action_item != "***" and action_no != '00' or test_data_item == "***" and \
                action_item != "***" and action_no != '00':

            if len(getdescp) == 1:
                elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity = getdescp[0]
                datax = locatorIdentity + '|' + elementIdentity + '|' + actionIdentity + '|' + actionxdesc + '|' + \
                        tstepx + '|' + action_item + '|' + test_data_item + '|' + felements + '|' + itemIdentity + \
                        '|' + id_generator()
                data.append(datax)
                # jsonfile.write(str(datax) + '\n')
            else:
                for xdata in range(len(getdescp)):
                    elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity = getdescp[xdata]
                    actionDesp, aItem, tItem = str(actiondesc).split('&'), str(action_item).split('&'), str(test_data_item).split('&')
                    datax = locatorIdentity + '|' + elementIdentity + '|' + actionIdentity + '|' + actionDesp[xdata] + '|' + \
                            tstepx + '|' + aItem[xdata] + '|' + tItem[xdata] + '|' + felements + '|' + itemIdentity + \
                            '|' + id_generator()
                    data.append(datax)
                    # jsonfile.write(str(datax) + '\n')
        elif action_no == '00' and action_item != "***":
            datax = 'None|None|None|' + actionxdesc + '|' + \
                    tstepx + '|' + action_item + '|' + test_data_item + '|None|None|' + id_generator()
            data.append(datax)
            # jsonfile.write(str(datax) + '\n')
        else:
            data = data
        # print(data)
        return data
    except Exception as e:
        return 'Error : ' + str(e)


def get_action_description(get_excel_data, action_description, ptname):
    getdesp=[]
    if '&' in action_description:
        get_action = action_description.split('&')
        for actiondesc in get_action:
            for xdescrip in range(0, len(get_excel_data)):
                if get_excel_data[xdescrip]['Description'] == actiondesc:
                    if ptname in ['Android', 'iOS']:
                        if ptname == 'Android':
                            elementIdentity = get_excel_data[xdescrip]['Elements1']
                        else:
                            elementIdentity = get_excel_data[xdescrip]['Elements2']
                    else:
                        elementIdentity = get_excel_data[xdescrip]['Elements']
                    locatorIdentity = get_excel_data[xdescrip]['Locators']
                    actionIdentity = get_excel_data[xdescrip]['Action']
                    description = get_excel_data[xdescrip]['Description']
                    felements = get_excel_data[xdescrip]['FetchElements']
                    itemIdentity = get_excel_data[xdescrip]['Item']
                    getx = elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity
                    getdesp.append(getx)
                    # print(getdesp)
    else:
        for xdescrip in range(0, len(get_excel_data)):
            if action_description == get_excel_data[xdescrip]['Description']:
                if ptname in ['Android', 'iOS']:
                    if ptname == 'Android':
                        elementIdentity = get_excel_data[xdescrip]['Elements1']
                    else:
                        elementIdentity = get_excel_data[xdescrip]['Elements2']
                else:
                    elementIdentity = get_excel_data[xdescrip]['Elements']
                locatorIdentity = get_excel_data[xdescrip]['Locators']
                actionIdentity = get_excel_data[xdescrip]['Action']
                description = get_excel_data[xdescrip]['Description']
                felements = get_excel_data[xdescrip]['FetchElements']
                itemIdentity = get_excel_data[xdescrip]['Item']
                getx = elementIdentity, locatorIdentity, actionIdentity, description, felements, itemIdentity
                getdesp.append(getx)
                break
    # print(getdesp)
    return getdesp
