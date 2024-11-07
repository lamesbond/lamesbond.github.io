from datetime import datetime
import os
import re
from xml.dom import minidom
from lxml import etree
from generate_rss import format_xml

#False选项就不转义特殊字符
parser = etree.XMLParser(strip_cdata=False)

directory = "/opt/lamesbond.github.io/xmls/fanpai-erpangfeng"

# 遍历指定目录中的每个 XML 文件
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        # 获取文件的绝对路径
        file_path = os.path.join(directory, filename)
        # 从文件名去除扩展名作为标题
        title_text = os.path.splitext(filename)[0]

        # 解析 XML 文件
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        
        pretty_xml = format_xml(root)
        # rough_xml = etree.tostring(root, encoding="utf-8", xml_declaration=False, pretty_print=True).decode("utf-8")
        # pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")
        # 将格式化后的 XML 拆分为行
        # pretty_xml_no_declaration = "\n".join(pretty_xml.splitlines()[1:])
        # print(pretty_xml_no_declaration)
        # 使用正则去掉多余的空行
        # cleaned_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)
        # cleaned_xml = cleaned_xml.replace("<description>", "<description>\n")
        # cleaned_xml = cleaned_xml.replace("</description>", "\n" + " " * 2 + "</description>")
        cleaned_xml = re.sub(r"影片《(.*?)重要信息", r"\n影片《\1重要信息", pretty_xml)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_xml)
