from datetime import datetime
import os
import re
from xml.dom import minidom
import lxml.etree

#False选项就不转义特殊字符
parser = lxml.etree.XMLParser(strip_cdata=False)

directory = "/opt/lamesbond.github.io/xmls/fanpai-other"

# 遍历指定目录中的每个 XML 文件
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        # 获取文件的绝对路径
        file_path = os.path.join(directory, filename)
        
        # 去掉文件的后缀，得到新 title 的内容
        new_title = os.path.splitext(filename)[0]
        
        # 解析 XML 文件
        tree = lxml.etree.parse(file_path, parser)
        root = tree.getroot()
        # 查找 description 元素并用 CDATA 包装内容
        description = root.find('.//description')
        if description is not None:
            description_text = description.text.strip() if description.text else ""
            description.clear()  # 清空内容

            description.text = lxml.etree.CDATA(description_text) # 用 CDATA 包装文本内容 
            print("描述：",description.text)
            # tree.write(file_path, encoding="UTF-8")
            # 转换为字符串并使用 pretty_print 进行初步格式化
        rough_xml = lxml.etree.tostring(root, encoding="utf-8", xml_declaration=False, pretty_print=True).decode("utf-8")

        pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")
        pretty_xml_no_declaration = "\n".join(pretty_xml.splitlines()[1:])
        print(pretty_xml_no_declaration)
        # 使用正则去掉多余的空行
        cleaned_xml = re.sub(r'\n\s*\n', '\n', pretty_xml_no_declaration)
        cleaned_xml = cleaned_xml.replace("<description>", "<description>\n")
        cleaned_xml = cleaned_xml.replace("</description>", "\n  </description>")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_xml)
