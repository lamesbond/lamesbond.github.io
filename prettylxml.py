from lxml import etree

# 创建根元素
root = etree.Element("root")

# 创建 description 元素
description_element = etree.SubElement(root, "description")

# 设置 CDATA 内容
cdata_content = "这是第一行。\n这是第二行。\n这是第三行。"
# 使用 text 属性插入 CDATA
description_element.text = etree.CDATA(cdata_content)

# 将 XML 转换为字符串，指定 pretty_print 为 True
xml_string = etree.tostring(root, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode('UTF-8')

# 输出结果
print(xml_string)
