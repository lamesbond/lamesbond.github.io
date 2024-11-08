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
    pretty_xml = minidom.parseString(rootstring).toprettyxml(indent="  ")

    # 按行分割，便于逐行处理
    lines = pretty_xml.splitlines()
    
    # 标志位：检测是否在 CDATA 区域
    in_cdata_section = False
    processed_lines = []
    
    for line in lines:
        # 检查 CDATA 区域的开始
        if "<![CDATA[" in line:
            in_cdata_section = True
        # 检查 CDATA 区域的结束
        if "]]>" in line:
            in_cdata_section = False
            processed_lines.append(line)
            continue
        
        # 如果在 CDATA 区域内，直接保留该行
        if in_cdata_section or line.strip():
            processed_lines.append(line)
    
    # 将处理后的行重新拼接为完整的 XML 字符串
    return "\n".join(processed_lines)

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
# 将结果保存到文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(rss_xml)
print("RSS 文件已成功生成：", output_file)