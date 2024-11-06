from datetime import datetime
import os
import re
from xml.dom import minidom
import lxml.etree

#False选项就不转义特殊字符
parser = lxml.etree.XMLParser(strip_cdata=False)

directory = "/opt/lamesbond.github.io/xmls/fanpai-erpangfeng"

# 遍历指定目录中的每个 XML 文件
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        # 获取文件的绝对路径
        file_path = os.path.join(directory, filename)
        # 从文件名去除扩展名作为标题
        title_text = os.path.splitext(filename)[0]

        # 解析 XML 文件
        tree = lxml.etree.parse(file_path, parser)
        root = tree.getroot()
        # 查找 <title> 元素并更新文本
        title_element = root.find(".//title")
        if title_element is not None:
            title_element.text = title_text
        # 查找 description 元素并用 CDATA 包装内容 
        # description = root.find('.//description')
        # if description is not None:
        #     description_text = description.text.strip() if description.text else ""
        #     # 逐行处理去掉前面的空格
        #     cleaned_cdata = "\n".join([line.lstrip() for line in description_text.splitlines()])
        #     description.clear()  # 清空内容

        #     description.text = lxml.etree.CDATA(cleaned_cdata) # 用 CDATA 包装文本内容 

        rough_xml = lxml.etree.tostring(root, encoding="utf-8", xml_declaration=False, pretty_print=True).decode("utf-8")

        pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")
        # 将格式化后的 XML 拆分为行
        pretty_xml_no_declaration = "\n".join(pretty_xml.splitlines()[1:])
        # print(pretty_xml_no_declaration)
        # 使用正则去掉多余的空行
        cleaned_xml = re.sub(r'\n\s*\n', '\n', pretty_xml_no_declaration)
        cleaned_xml = cleaned_xml.replace("<description>", "<description>\n")
        cleaned_xml = cleaned_xml.replace("</description>", "\n" + " " * 2 + "</description>")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_xml)
