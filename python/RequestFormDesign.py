from unicodedata import name
import formDesignBase as base
import requests
import simplejson
"""
    ---------------------------------GLOBAL---------------------------------
"""
getUrl = base.getUrl
addUrl = base.addUrl
addsUrl = base.addsUrl

"""
    -----------------------------------------------------星火站-处理热图数据-----------------------------------------------------------------------------
"""

xhzWorksheetConf = {
    # 监测点id
    "monitorWSId": "61e4c2bedf74914eba804421",
    # 监测数据id
    "monitorDataWSId": "61e11ea7df74914eba7c2e26",
    # 热图数据id
    "hotMapWSId": "620dbc3b1d65ebe4a235bcb6"
}
# 监测点字段
xhzMonitorsFieldContrast = {
    "name": "input_1642130110497",
    "x": "number_1642130114900",
    "y": "number_1642130115293",
    "z": "number_1642130115686",
}
# 监测数据字段
xhzMonitorDataFieldContrast = {
    "name": "input_1642143376509",
    "value": "number_1642143386641",
    "sortedId": "date_1642143391431"
}
# 热图字段
xhzHotMapFieldContrast = {
    "name": "input_1645067305392",
    "x": "number_1645067309975",
    "y": "number_1645067312525",
    "z": "number_1645067314908",
    "value": "number_1645067318558",
}


def updateHotMap():
    # 监测点名称
    monitors = {}
    # 查询所有的监测点
    monitorsConf = base.initFormDesignConf(
        xhzWorksheetConf["monitorWSId"], "list")
    hotMapConf = base.initFormDesignConf(xhzWorksheetConf["hotMapWSId"], "adds")

    monitorsConf2 = simplejson.dumps(monitorsConf)
    res = requests.post(url=getUrl, data=monitorsConf2, headers={
                        'Content-Type': 'application/json;charset=UTF-8'})

    result = res.json()
    if result["code"] == 200:
        datas = result["data"]
        for data in datas:
            monitorName = data[xhzMonitorsFieldContrast["name"]]
            if monitors.get(monitorName) is None:
                monitors[monitorName] = [
                    {"x": data[xhzMonitorsFieldContrast["x"]],
                     "y":data[xhzMonitorsFieldContrast["y"]],
                     "z":data[xhzMonitorsFieldContrast["z"]]}
                ]
            else:
                monitors[monitorName].append({"x": data[xhzMonitorsFieldContrast["x"]],
                                              "y": data[xhzMonitorsFieldContrast["y"]],
                                              "z": data[xhzMonitorsFieldContrast["z"]]})

        # 根据监测点名称查询最新值
        monitorsDataConf = base.initFormDesignConf(
            xhzWorksheetConf["monitorDataWSId"], "list")
        monitorsDataConf["sortField"] = xhzMonitorDataFieldContrast["sortedId"]
        monitorsDataConf["pageSize"] = 1
        monitorsDataConf["filters"] = [{"id": 0, "field": xhzMonitorDataFieldContrast["name"],
                                        "dataType": 0, "spliceType": 0, "filterType": 2, "values": []}]

        addRows = []
        for key in monitors.keys():
            monitorsDataConf["filters"][0]["values"] = [key]
            monitorsDataConf2 = simplejson.dumps(monitorsDataConf)
            res2 = requests.post(url=getUrl, data=monitorsDataConf2, headers={
                'Content-Type': 'application/json;charset=UTF-8'})
            res3 = res2.json()
            # 查询到最新数据
            if res3["code"] == 200 and len(res3["data"]) > 0:
                print("查询 %s 成功！" % (key))
                rValue = res3["data"][0][xhzMonitorDataFieldContrast["value"]]
                for a in monitors[key]:
                    addRows.append({
                        xhzHotMapFieldContrast["name"]: key,
                        xhzHotMapFieldContrast["x"]: a["x"],
                        xhzHotMapFieldContrast["y"]: a["y"],
                        xhzHotMapFieldContrast["z"]: a["z"],
                        xhzHotMapFieldContrast["value"]: rValue
                    })
        hotMapConf["rows"] = addRows
        hotMapConf2 = simplejson.dumps(hotMapConf)
        res = requests.post(url=addsUrl, data=hotMapConf2, headers={
            'Content-Type': 'application/json;charset=UTF-8'})
        print(res.json())
    # 根据名称
    else:
        print(result)





if __name__ == '__main__':
    # 处理热图数据
    updateHotMap()
