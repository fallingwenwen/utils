import ctBase as base
import requests
import simplejson
import re


"""
    ---------------------------------GLOBAL---------------------------------
"""
getUrl = base.getUrl
addsUrl = base.appAddsUrl
fdStructureUrl = base.structureUrl
fieldContrastByCode = {}
"""
    -----------------------------------------------------CONFIG-----------------------------------------------------------------------------
"""
transferWSId = {
    # APPID
    "transferWSId": "62120913f3faa72fd5906cc2",
    # formDesignID
    "baseWSId": "61ed28670fb63674a6b7ca6b",
    # mdID
    "mdWSId": "5fbb0df61609f80bf8e811fe"
}
# 左边是APP的字段，右边是formDesign的字段
fieldContrast = {
    "number19842": "number_1642990590289",
    "number89071": "number_1642990581415",
    "number23683": "number_1642990581803",
    "number107254": "number_1642990582335"
}
"""
    -----------------------------------------------------FUNCTION-----------------------------------------------------------------------------
"""
# 获取到formDesign的表单数据
formDesignData = []
# 要添加的表单数据 [[],[],[]]
addRows = [[]]


def formDesign2APP():
    global fieldContrastByCode
    global formDesignData
    global addRows
    # 获取formDesign的数据
    baseFormDesignConf = base.initFormDesignConf(
        transferWSId["baseWSId"], "list")
    baseFormDesignConf2 = simplejson.dumps(baseFormDesignConf)
    baseResult = requests.post(url=getUrl, data=baseFormDesignConf2)
    if(baseResult.json()["code"]) == 200:
        formDesignData = baseResult.json()["data"]

    # 处理要添加的数据
    for row in formDesignData:
        addDic = {}
        for k in fieldContrastByCode:
            if(row.get(fieldContrastByCode[k]) is None):
                addDic[k] = ""
                continue
            if("date" in k):
                addDic[k] = re.sub(r"/", "-", row.get(fieldContrastByCode[k]))
                continue
            addDic[k] = row[fieldContrastByCode[k]]
        if(len(addRows[len(addRows)-1])) > 1999:
            addRows.append([])
        addRows[len(addRows)-1].append(addDic)

    # 向APP中添加数据
    transferConf = base.initFormDesignConf(
        transferWSId["transferWSId"], "adds"
    )
    for addrow in addRows:
        transferConf["rows"] = addrow
        transferConf3 = simplejson.dumps(transferConf)
        transferResult = requests.post(url=addsUrl, data=transferConf3, headers={
            'Content-Type': 'application/json;charset=UTF-8'})
        print(transferResult.json())


def contrastField():
    global fieldContrastByCode
    appColumns = []
    fdColumns = []

    # app结构
    appStructure = base.getStructure(transferWSId["transferWSId"], "app")
    for i in appStructure:
        appColumns.append(i["name"])

    # formDesign结构
    fdStructure = base.getStructure(transferWSId["baseWSId"], "fd")
    for i in fdStructure:
        fdColumns.append(i["name"])
    
    for index,item in enumerate(appColumns):
        fieldContrastByCode[item] = fdColumns[index]


"""
    将formDesign表单数据转移到APP表单
    使用配置：
        1.transferWSId

"""
if __name__ == '__main__':
    contrastField()
    formDesign2APP()
