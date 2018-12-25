from xml.etree import ElementTree as ET
from SPIMI import CleanData

def parsexml():
    querys = []
    weights = []
    # 打开xml文件并且解析，返回一个xml.etree.ElementTree.ElementTree对象
    tree = ET.parse("topics.xml")
    # 获取xml的根节点
    root = tree.getroot()

    for value in root.iter("topic"):
        query = ""
        weight = []
        for i in range(4):
            temp = CleanData(value[i].text)
            query += temp + " "
            weight.append(len(temp.split()))
        query.rstrip()
        weights.append(weight)
        querys.append(query)
    return querys, weights


def parsexml1():
    querys = []
    # 打开xml文件并且解析，返回一个xml.etree.ElementTree.ElementTree对象
    tree = ET.parse("topics.xml")
    # 获取xml的根节点
    root = tree.getroot()

    for value in root.iter("topic"):
        query = {}
        for i in range(4):
            temp = CleanData(value[i].text)
            query[i] = temp
        querys.append(query)
    return querys