import os
import re
from xml.dom import minidom
from lxml import etree

#False选项就不转义特殊字符
parser = etree.XMLParser(strip_cdata=False)
# 主文件路径
showinfo_file = "/opt/lamesbond.github.io/showinfo.xml"
# 单集文件目录
episode_dir = "/opt/lamesbond.github.io/xmls/"
# 输出文件路径
output_file = "/opt/lamesbond.github.io/rss.xml"

# 解析 XML 文件
rss_tree = etree.parse(showinfo_file, parser)
rss_root = rss_tree.getroot()
print(etree.tostring(rss_root, encoding="utf-8").decode("utf-8"))

# 获取 <channel> 标签
channel = rss_root.find("channel")

def format_xml(root):
    rootstring = etree.tostring(root, encoding="utf-8", xml_declaration=False, pretty_print=True).decode("utf-8")

    # 使用 re.findall 匹配多个 CDATA 区域
    # cdata_matches = re.findall(r'<!\[CDATA\[(.*?)\]\]>', rootstring, re.DOTALL)
    # Step 1: 使用 re.findall 匹配并保留 CDATA 标记
    cdata_matches = re.findall(r'<!\[CDATA\[[^\]]*\]\]>', rootstring, re.DOTALL)
    # Step 2: 使用占位符替换原字符串中的 CDATA 区域
    modified_string = rootstring
    for i, cdata in enumerate(cdata_matches, 1):
        placeholder = f"CDATA_PLACEHOLDER_{i}"
        modified_string = modified_string.replace(cdata, placeholder)

    # 使用 minidom 进行格式化
    pretty_xml = minidom.parseString(modified_string).toprettyxml(indent="  ")
    pretty_xml = "\n".join(pretty_xml.splitlines()[1:])  #删除第一行
    pretty_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)  # 删除多余的空行

    # Step 3: 替换占位符为原来的 CDATA 内容
    for i, cdata in enumerate(cdata_matches, 1):
        placeholder = f"CDATA_PLACEHOLDER_{i}"
        pretty_xml = pretty_xml.replace(placeholder, cdata)

    return pretty_xml

# 迭代单集文件
for dirpath, dirnames, filenames in os.walk(episode_dir):
    for filename in filenames:
        episode_path = os.path.join(dirpath, filename)
        if filename.endswith(".xml"):
            # 解析单集文件并找到 <item>
            episode_tree = etree.parse(episode_path,parser)
            episode_root = episode_tree.getroot()
            # 将顶级 <item> 直接添加到 <channel>
            # 确保根元素是 <item>，并清除不需要的属性
            if episode_root.tag == 'item':
                # 清除声明属性
                episode_root.attrib.pop('version', None)
                episode_root.attrib.pop('encoding', None)
            channel.append(episode_root)

rss_xml = format_xml(rss_root)
with open("rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

# 将结果保存到文件
# with open(output_file, "w", encoding="utf-8") as f:
    # f.write(cleaned_xml)
# print("RSS 文件已成功生成：", output_file)
