import requests
import json

getUrl = r"http://39.98.119.248:8880/api/v2/open/worksheet/getFilterRows"
addUrl = r"http://39.98.119.248:8880/api/v2/open/worksheet/addRow"
addsUrl = r"http://39.98.119.248:8880/api/v2/open/worksheet/addRows"
structureUrl = r"http://39.98.119.248:8880/api/v2/open/worksheet/getWorksheetInfo"


def getBaseConf(wsId):
    return {
        "appKey": "4b20f7647008eb45",
        "sign": "NGRlYjE3OGM0YTI5YmE2MjY5MTM0YWFmYmY2ODZlNDdiMDcxODdkYzVkMWI3ZjgzMzgzZDhhNzk4ODkwNmRjMA==",
        "worksheetId": wsId
    }


def initConf(wsId, type):
    baseConf = getBaseConf(wsId)
    listConf = {
        "pageSize": 99999,
        "pageIndex": 1,
        "sortId": "",
        "isAsc": False,
        "keywords": "",
        "filters": []
    }

    if type == "list":
        baseConf.update(listConf)
    elif type == "add":
        print("add")
    elif type == "adds":
        print("adds")
    elif type == "del":
        print("del")
    return baseConf


def getStructure(wsId):
    baseConf = getBaseConf(wsId=wsId)
    baseResult = requests.post(
        url=structureUrl, data=json.dumps(baseConf), headers={
            'Content-Type': 'application/json;charset=UTF-8'})
    if baseResult.json()["success"] == True:
        return baseResult.json()["data"]["controls"]
    else:
        return None


if __name__ == '__main__':
    getStructure("62120ae43a00e213d0e89136")
