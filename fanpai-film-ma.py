import xml.etree.ElementTree as ET

# XML 文件路径
xml_file_path = "/opt/lamesbond.github.io/fanpai-film-ma.xml"  # 替换为你的文件路径

# 解析 XML 文件
tree = ET.parse(xml_file_path)
root = tree.getroot()

# 找到所有 <item> 元素
items = root.findall('.//item')

# 提取每个 <item> 的 <title> 和 <link>
for item in items:
    title = item.find('title').text if item.find('title') is not None else '无标题'
    link = item.find('link').text if item.find('link') is not None else '无链接'
    print(f'Title: {title}\nLink: {link}\n')
