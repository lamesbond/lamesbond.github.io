import json
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

# 将毫秒转为 HH:MM:SS 格式的函数
def convert_duration_to_hhmmss(duration_ms):
    total_seconds = duration_ms // 1000  # 将毫秒转换为秒
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}:{minutes:02}:{seconds:02}"  # 格式化为 HH:MM:SS

# 指定 JSON 文件路径
json_file_path = "/opt/fanpaifilm/episodes.json"  # 替换为你的 JSON 文件路径
output_directory = "/opt/fanpaifilm/xmls"  # 输出 XML 文件的目录

# 创建输出目录（如果不存在）
os.makedirs(output_directory, exist_ok=True)

# 添加命名空间
ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')

# 从 JSON 文件读取数据
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data_list = json.load(json_file)  # 加载 JSON 数据为列表

# 遍历每个条目
for item_data in data_list:
    # 创建 XML 元素，并添加命名空间
    item_element = ET.Element("item", xmlns="http://www.itunes.com/dtds/podcast-1.0.dtd")
    
    # 添加标题
    title_element = ET.SubElement(item_element, "title")
    title_element.text = item_data.get("title", "")

    # 添加链接
    link_element = ET.SubElement(item_element, "link")
    link_element.text = item_data.get("link", "")

    # 添加图片
    # image_element = ET.SubElement(item_element, "itunes:image", href="https://media.wavpub.com/15/7e/06/20241010010416-hBdbDQSbsshrdZUE.jpg")

        # 添加 <itunes:image> 元素
    image_element = ET.SubElement(item_element, "{http://www.itunes.com/dtds/podcast-1.0.dtd}image")
    image_element.set("href", item_data.get("image", ""))

    #添加分级
    # explicit_element = ET.SubElement(item_element, "itunes:explicit")
    # explicit_element.text = "false"

    # 添加描述;
    description_element = ET.SubElement(item_element, "description")
    description_element.text = item_data.get("description", "") + "\n"
    
    # 添加 pubDate
    pub_date_element = ET.SubElement(item_element, "pubDate")
    pub_date_element.text = item_data.get("datePublishedPretty", "")
    
    # 添加 enclosure
    enclosure_element = ET.SubElement(item_element, "enclosure", {
        "url": item_data.get("enclosureUrl", ""),
        "type": item_data.get("enclosureType", "")
    })
    
    # 添加 itunes:duration
    duration_ms = item_data.get("duration", 0)  # 获取 duration 字段
    itunes_duration = convert_duration_to_hhmmss(duration_ms)  # 转换为时长格式
    duration_element = ET.SubElement(item_element, "{http://www.itunes.com/dtds/podcast-1.0.dtd}duration")
    duration_element.text = itunes_duration

    # 生成 XML 树
    tree = ET.ElementTree(item_element)
    

    # # 使用 minidom 格式化 XML
    xml_str = ET.tostring(item_element, encoding='utf-8', xml_declaration=True).decode('utf-8')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

    # # 获取标题并清理文件名（替换不适合的字符）
    file_name = item_data.get("title", "Untitled").replace("/", "-").replace("\\", "-") + ".xml"
    file_path = os.path.join(output_directory, file_name)
    # tree.write(file_path, encoding='utf-8', xml_declaration=True)

    # # 将格式化后的 XML 写入文件
    with open(file_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(pretty_xml_str)





print("所有条目已成功写入 XML 文件。")
