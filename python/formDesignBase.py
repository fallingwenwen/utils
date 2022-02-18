getUrl = r"http://39.98.252.137:4600/api/v1/worksheet/getFilterRows"
addUrl = r"http://39.98.252.137:4600/api/v1/worksheet/addRow"
addsUrl = r"http://39.98.252.137:4600/api/v1/worksheet/addRows"
appAddsUrl = r"http://39.98.252.137/api/v2/worksheet/addRows"


def getBaseConf(wsId):
    return {
        "App-Key": "6041cc9f9680c46862f4efb6",
        "Sign": "qHGMOhRDCxV-x57.9CoWFl5G3Hp9HDNR8KG.ZosSpKxQ9HW5KQC98z71cW9nVC284ne4K4uPmX1NmmhP7cK4nCe2JI2p50TEH9z6U93stk.hUmq0act0HQh6IpjalSBC",
        "worksheetId": wsId
    }


def initFormDesignConf(wsId, type):
    baseConf = getBaseConf(wsId)
    listConf = {
        "pageSize": 99999,
        "pageNo": 1,
        "sortField": "",
        "isAsc": False,
        "keywords": "",
        "filters": []
    }
    addConf = {
        "data": {}
    }
    addsConf = {
        "rows": []
    }
    delConf = {
        "rowId": ""
    }
    if type == "list":
        baseConf.update(listConf)
    elif type == "add":
        baseConf.update(addConf)
    elif type == "adds":
        baseConf.update(addsConf)
    elif type == "del":
        baseConf.update(delConf)
    return baseConf
