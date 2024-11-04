import xml.etree.ElementTree as ET

# 只注册命名空间
ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")

# 创建根元素，不显式添加 xmlns:itunes
root = ET.Element("rss")

# 创建不带命名空间的子元素
child = ET.SubElement(root, "wenhouyu")
child.text = "Hello World!"

# 创建带命名空间的子元素
child = ET.SubElement(root, "{http://www.itunes.com/dtds/podcast-1.0.dtd}wenhouyu")
child.text = "aloha!"

# 生成 XML 对方文档
xml_str = ET.tostring(root, encoding="utf-8")
print(xml_str.decode("utf-8"))
# 写入到文件 sample.xml
tree = ET.ElementTree(root)
tree.write("sample.xml", encoding="UTF-8", xml_declaration=True)