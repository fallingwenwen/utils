import os
import pandas as pd
import requests
import simplejson
import ctBase as ct
import  re
from datetime import datetime

df = ''


def resolveXlsx(baseDir, column):
    global addsFormConfig
    global df
    for root, dirs, files in os.walk(baseDir):
        for file in files:
            # 获取文件路径
            filePath = os.path.join(root, file)
            print("开始上传文件：%s" % filePath)
            if filePath.endswith("csv"):
                df = pd.read_csv(filePath)
            elif filePath.endswith("xlsx"):
                df = pd.read_excel(io=filePath)
            # 从df中取指定列
            newDF = df[column]
            contact = [[]]
            # 第i行
            for i in newDF.index.values:
                # 每个数组不得多余100条记录
                if len(contact[len(contact) - 1]) == 100:
                    contact.append([])
                # 第j列
                singleRowColumn = baseConfig["row"]
                for j in range(0, len(column)):
                    dictKey = list(singleRowColumn.keys())[j]
                    # 第i行第j列
                    v = newDF.iloc[i, j]
                    if "date" in dictKey:
                        singleRowColumn[dictKey] = re.sub("/", "-", v)
                        # singleRowColumn[dictKey] = str(
                        #     datetime.strptime(v, '%Y/%m/%d'))
                    else:
                        singleRowColumn[dictKey] = v
                contact[len(contact) - 1].append(singleRowColumn)
            for rows in contact:
                addsFormConfig["rows"] = rows
                data = simplejson.dumps(addsFormConfig)
                res = requests.post(ct.appAddsUrl, headers={'Content-Type': 'application/json;charset=UTF-8'},
                                    data=data)
                print('upload row success \n     message：%s' % (res.text))


baseConfig = {
    "type": "app",
    "method": "adds",
    "wsId": "6209ca581712907f63e45f84",
    "row": {
        "input51325": "文本",
        "select27427": "文本",
        "number30644": 123.45,
        "date62362": "2006-01-02 15:04:05",
        "select76129": "文本"
    },
    "baseDir": r"D:\project\北京市政\星火站\历史监测数据\周上传数据\20220328\施工方\星火站\网页数据",
    "column": ["测点名称", "测点类型","累计沉降（mm）","监测时间","区间"]
    # "column": ["测点名称","测点类型","监测时间","区间"]
}
addsFormConfig = ct.initFormDesignConf(
    baseConfig["wsId"], baseConfig["method"]
)
"""
    使用方式:
        1.配置baseConfig下的wsId,row,baseDir,column
    参数详解: 
        wsId: app的worksheetId
        row: 批量添加时的字段
        baseDir: 基础目录
        column: 取的excel中的列名
    注意事项: 
        row的顺序和column的顺序需要对照
"""
if __name__ == '__main__':
    resolveXlsx(baseConfig["baseDir"], baseConfig["column"])
