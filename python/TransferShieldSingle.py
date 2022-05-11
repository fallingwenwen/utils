import simplejson
from assets.UtillClass import UtillClass


class TransferShieldSingle(UtillClass):
    """生成一条盾构数据并添加到另一张表单中
    """

    def __init__(self,  *args):
        super()
        self.APP = "6041cc9f9680c46862f4efb6"
        self.SIGN = "qHGMOhRDCxV-x57.9CoWFl5G3Hp9HDNR8KG.ZosSpKxQ9HW5KQC98z71cW9nVC284ne4K4uPmX1NmmhP7cK4nCe2JI2p50TEH9z6U93stk.hUmq0act0HQh6IpjalSBC"
        self.filterUrl = "https://mapchang.com/api/v2/worksheet/getFilterRows"
        self.addUrl = "https://mapchang.com/api/v2/worksheet/addRow"
        # 源表单
        self.source = {
            "wsid": "620a0abb1712907f63e6f98b",
            "id": "number_288"
        }
        # 目标 表单
        self.target = {
            "wsid": "627b59b1de215adf9b3a85f8",
            "id": "number40766"
        }
        # 左边是source  右边是target
        self.fieldsContrast = {
            # 环号
            "number_288": "number40766",
            # 记录时间
            "date_1640740674883": "date50222",
            # 注浆累计(环)
            "number_1207": "number110181",
            # 土舱土压（左上）
            "number_39": "number35195",
            # 俯仰角（前筒体）
            "number_903": "number104799"
        }

    def _addCurrentRing(self, ring):
        # 源 当前环
        sourceTemplate = self._getFilterTemplate()
        sourceTemplate["worksheetId"] = self.source["wsid"]
        sourceFilters = self._getSourceFilter()
        sourceFilters[0]["values"] = [str(ring)]
        sourceTemplate["filters"] = sourceFilters
        sourceRows = self.rq(self.filterUrl, sourceTemplate)
        if sourceRows:
            # 生成添加的data
            sourceRow = sourceRows[0]
            data = {}
            for key, value in self.fieldsContrast.items():
                if sourceRow[key]:
                    data[value] = sourceRow[key]
            addTemplate = self._getAddTemplate()
            addTemplate["worksheetId"] = self.target["wsid"]
            addTemplate["data"] = data
            result = self.request(self.addUrl, addTemplate)
            print("add %s 环 success!" % ring)
        else:
            print("空环 %s" % ring)

    def _getSourceFilter(self):
        """获取源过滤条件

        Returns:
            array: 过滤条件
        """
        return [{
                "dataType": 5,
                "dateRange": 1,
                "field": "number_288",
                "filterType": 2,
                "spliceType": 0,
                "uuid": "eris469kt",
                "value": 0,
                "values": []
                }]

    def _getLatestRing(self, wsid, ringColumn):
        """查找最新环

        Args:
            wsid (str): 表单id
            ringColumn (int): 环号

        Returns:
            int: 环号
        """
        template = self._getFilterTemplate()
        template["sortField"] = ringColumn
        template["worksheetId"] = wsid
        result = self.rq(self.filterUrl, template)
        if(result is not None):
            return result[0][ringColumn]
        else:
            return result

    def _getFilterTemplate(self):
        """过滤查询模板

        Returns:
            JSON: 过滤查询模板
        """
        return {
            "App-Key": self.APP,
            "Sign": self.SIGN,
            "worksheetId": "",
            "pageSize": 10,
            "pageNo": 1,
            "sortField": "",
            "keywords": "",
            "filters": []
        }

    def _getAddTemplate(self):
        return {
            "App-Key": self.APP,
            "Sign": self.SIGN,
            "worksheetId": "",
            "data": {
            }
        }


if __name__ == '__main__':
    tss = TransferShieldSingle()
    # 源最新环
    sourceLatestRing = tss._getLatestRing(tss.source["wsid"], tss.source["id"])
    # 目标最新环
    # targetLatestRing = tss._getLatestRing(tss.target["wsid"], tss.target["id"])
    # if targetLatestRing is None:
    # targetLatestRing = 1
    targetLatestRing = 68
    for ring in range(targetLatestRing, sourceLatestRing+1):
    # 查询当前环的参数
        tss._addCurrentRing(ring)
