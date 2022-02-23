import ctBase as base
import mdBase as md
import requests
import simplejson
import re


"""
    ---------------------------------GLOBAL---------------------------------
"""
appAddsUrl = base.appAddsUrl
fdStructureUrl = base.structureUrl
fieldContrastByCode = {}
"""
    -----------------------------------------------------CONFIG-----------------------------------------------------------------------------
"""
transferWSId = {
    # APPID
    "transferWSId": "62120913f3faa72fd5906cc2",
    # mdID
    "mdWSId": "62120ae43a00e213d0e89136"
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
    # 获取md的数据
    baseFormDesignConf = md.initConf(transferWSId["mdWSId"], "list")
    baseFormDesignConf2 = simplejson.dumps(baseFormDesignConf)
    baseResult = requests.post(url=md.getUrl, data=baseFormDesignConf2,headers={
            'Content-Type': 'application/json;charset=UTF-8'})

    if(baseResult.json()["success"]) == True:
        formDesignData = baseResult.json()["data"]["rows"]

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
        transferResult = requests.post(url=appAddsUrl, data=transferConf3, headers={
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

    # md结构
    fdStructure = md.getStructure(transferWSId["mdWSId"])
    for i in fdStructure:
        fdColumns.append(i["controlId"])
    
    for index,item in enumerate(appColumns):
        fieldContrastByCode[item] = fdColumns[index]


"""
    将MD表单数据转移到APP表单
    使用配置：
        1.transferWSId
        2.配置明道的appKey和Sign

"""
if __name__ == '__main__':
    contrastField()
    formDesign2APP()
