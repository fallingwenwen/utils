import formDesignBase as base
import requests
import simplejson
import re

"""
    ---------------------------------GLOBAL---------------------------------
"""
getUrl = base.getUrl
addsUrl = base.appAddsUrl
"""
    -----------------------------------------------------CONFIG-----------------------------------------------------------------------------
"""
transferWSId = {
    "baseWSId": "61eceb7240b9a12c9e1afe05",
    "transferWSId": "620f6734f3faa72fd58c424e"
}
# 左边是APP的字段，右边是formDesign的字段
fieldContrast = {
    "input71202": "input_1607658096853",
    "date42948": "input_1607658100224",
    "number66161": "number_1607658103501"
}
"""
    -----------------------------------------------------FUNCTION-----------------------------------------------------------------------------
"""
# 获取到formDesign的表单数据
formDesignData = []
# 要添加的表单数据 [[],[],[]]
addRows = [[]]


def formDesign2APP():
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
        for k in fieldContrast:
            if(row.get(fieldContrast[k]) is None):
                addDic[k] = ""
                continue
            if("date" in k):
                addDic[k] = re.sub(r"/", "-", row.get(fieldContrast[k]))
                continue
            addDic[k] = row[fieldContrast[k]]
        if(len(addRows[len(addRows)-1])) > 100:
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


"""
    将formDesign表单数据转移到APP表单
    使用配置：
        1.fieldContrast
        2.transferWSId

"""
if __name__ == '__main__':
    formDesign2APP()
