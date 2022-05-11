import simplejson
import requests


class UtillClass():
    def __init__(self) -> None:
        pass

    def rq(self, url, body):
        data = simplejson.dumps(body)
        res = requests.post(
            url, headers={'Content-Type': 'application/json;charset=UTF-8'},  data=data)
        if res.json()["code"] == 200 and res.json()["totalCount"] > 0:
            return res.json()["data"]
        else:
            return None

    def request(self, url, body):
        data = simplejson.dumps(body)
        res = requests.post(
            url, headers={'Content-Type': 'application/json;charset=UTF-8'},  data=data)
        return res.json()


if __name__ == '__main__':
    ul = UtillClass()
    body = {
        "App-Key": "6041cc9f9680c46862f4efb6",
        "Sign": "qHGMOhRDCxV-x57.9CoWFl5G3Hp9HDNR8KG.ZosSpKxQ9HW5KQC98z71cW9nVC284ne4K4uPmX1NmmhP7cK4nCe2JI2p50TEH9z6U93stk.hUmq0act0HQh6IpjalSBC",
        "worksheetId": "627b131fde215adf9b3a762c",
        "pageSize": 10,
        "pageNo": 1,
        "sortField": "",
        "keywords": "",
        "filters": []
    }
    ul.request(r"https://mapchang.com/api/v2/worksheet/getFilterRows", body)
