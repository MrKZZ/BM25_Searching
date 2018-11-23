from xml.etree import ElementTree as ET

def parsexml():
    querys = []
    # 打开xml文件并且解析，返回一个xml.etree.ElementTree.ElementTree对象
    tree = ET.parse("topics.xml")
    # 获取xml的根节点
    root = tree.getroot()

    for value in root.iter("topic"):
        query = ""
        for i in range(4):
            query += value[i].text + " "
        query.rstrip()
        querys.append(query)
    return querys
