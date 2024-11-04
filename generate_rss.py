import os
import re
from xml.dom import minidom
import xml.etree.ElementTree as ET

# 主文件路径
main_file = "/opt/lamesbond.github.io/showinfo.xml"
# 单集文件目录
episode_dir = "/opt/lamesbond.github.io/xmls/"
# 输出文件路径
output_file = "/opt/lamesbond.github.io/rss.xml"

# 解析主文件
ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
tree = ET.parse(main_file)
root = tree.getroot()

# 获取 <channel> 标签
channel = root.find("channel")

# 迭代单集文件
for episode_file in os.listdir(episode_dir):
    episode_path = os.path.join(episode_dir, episode_file)
    if episode_file.endswith(".xml"):
        # 解析单集文件并找到 <item>
        # print(episode_file)
        episode_tree = ET.parse(episode_path)
        episode_root = episode_tree.getroot()
        
#       去掉命名空间
        if episode_root.tag.startswith("{"):
            # 获取命名空间和标签名称
            episode_root.tag = episode_root.tag.split('}', 1)[1]  # 仅保留标签名称
        # 去掉属性
        episode_root.attrib.clear()  # 清除所有属性

        # 打印修改后的 episode_root 的内容
        # print("Modified Episode Root:", ET.tostring(episode_root, encoding='utf-8').decode('utf-8'))  # 打印修改后的 XML 内容

        # 将顶级 <item> 直接添加到 <channel>
        channel.append(episode_root)
        # channel.append(ET.Element("newline"))  # 插入一个新行元素作为占位符

# 保存到新的文件
# tree.write(output_file, encoding="UTF-8", xml_declaration=True)

# 生成字符串并格式化输出
rough_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
# 为 <description> 内容添加 CDATA 包裹
def wrap_description_with_cdata(match):
    description_content = match.group(2).strip()
    print("Description Content:", description_content)  # 打印 description_content
    indent = match.group(0)  # 获取 <description> 标签的缩进
    print("indent:", indent)  # 打印 indent
    # 使用 CDATA 包裹 description 内容
    cdata_content = f"<![CDATA[{description_content}]]>"
    return f"{match.group(1)}\n{cdata_content}\n{match.group(3)}"

desc_withcdata_xml = re.sub(r'(<description>)(.*?)(</description>)', wrap_description_with_cdata, rough_string, flags=re.DOTALL)
# 为每个 <item> 元素之间添加换行
# rss_xml_str = rough_string.replace("</item>", "</item>\n")
reparsed = minidom.parseString(desc_withcdata_xml)
pretty_xml = reparsed.toprettyxml(indent="  ")
# 使用正则去掉多余的空行
cleaned_xml = re.sub(r'\n\s*\n', '\n', pretty_xml)
# 为 <description> 内容添加额外缩进
# def add_indent_to_description(match):
#     description_content = match.group(2).strip()
#     indented_content = "\n        " + "\n        ".join(description_content.splitlines())
#     return f"{match.group(1)}{indented_content}\n    {match.group(3)}"

# cleaned_xml = re.sub(r'(<description>)(.*?)(</description>)', add_indent_to_description, cleaned_xml, flags=re.DOTALL)
# 为 <description> 内容添加换行符和 <br/> 标签
# def format_description(match):
#     description_content = match.group(2).strip()
#     formatted_content = "<br/>".join(description_content.splitlines())
#     return f"{match.group(1)}{formatted_content}{match.group(3)}"

# cleaned_xml = re.sub(r'(<description>)(.*?)(</description>)', format_description, cleaned_xml, flags=re.DOTALL)
# 移除 `<newline/>` 标签并添加实际换行符
# pretty_xml = pretty_xml.replace("<newline/>", "")

# 将结果保存到文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(cleaned_xml)
print("RSS 文件已成功生成：", output_file)
