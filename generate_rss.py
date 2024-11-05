import os
import re
from xml.dom import minidom
import lxml.etree

#False选项就不转义特殊字符
parser = lxml.etree.XMLParser(strip_cdata=False)
# 主文件路径
showinfo_file = "/opt/lamesbond.github.io/showinfo.xml"
# 单集文件目录
episode_dir = "/opt/lamesbond.github.io/xmls/"
# 输出文件路径
output_file = "/opt/lamesbond.github.io/rss.xml"

# 解析 XML 文件
rss_tree = lxml.etree.parse(showinfo_file, parser)
rss_root = rss_tree.getroot()
print(lxml.etree.tostring(rss_root, encoding="utf-8").decode("utf-8"))

# 获取 <channel> 标签
channel = rss_root.find("channel")

# 迭代单集文件
for dirpath, dirnames, filenames in os.walk(episode_dir):
    for filename in filenames:
        episode_path = os.path.join(dirpath, filename)
        if filename.endswith(".xml"):
            # 解析单集文件并找到 <item>
            episode_tree = lxml.etree.parse(episode_path,parser)
            episode_root = episode_tree.getroot()
            # 将顶级 <item> 直接添加到 <channel>
            # 确保根元素是 <item>，并清除不需要的属性
            if episode_root.tag == 'item':
                # 清除声明属性
                episode_root.attrib.pop('version', None)
                episode_root.attrib.pop('encoding', None)
            channel.append(episode_root)

# 生成字符串并格式化输出
rough_xml = lxml.etree.tostring(rss_root, encoding="utf-8", xml_declaration=False, pretty_print=True).decode("utf-8")

pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="  ")
pretty_xml_no_declaration = "\n".join(pretty_xml.splitlines()[1:])
# 使用正则去掉多余的空行
cleaned_xml = re.sub(r'\n\s*\n', '\n', pretty_xml_no_declaration)

# 将结果保存到文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(cleaned_xml)
print("RSS 文件已成功生成：", output_file)
