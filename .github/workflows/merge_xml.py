import xml.etree.ElementTree as ET
import os

# 定义要合并的 XML 文件名
xml_files = ['fanpai001-050.xml', 'fanpai051-100.xml']
output_file = 'rss.xml'

# 创建根元素
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')

# 解析并合并 XML 文件
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    channel_data = tree.find('channel')
    
    for item in channel_data.findall('item'):
        channel.append(item)

# 保存合并后的 XML 文件
tree = ET.ElementTree(rss)
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'Merged XML files into {output_file}')
