import os
import xml.etree.ElementTree as ET

# 设置 XML 文件所在的目录
xml_directory = "/opt/lamesbond.github.io/xmls"  # 替换为你的文件目录路径

# 设置新的链接地址
new_link = "https://weixin.xom"

def get_fanpai_title_link(xml_file_path):
    fanmai_title_link_list = []

    # 解析 XML 文件
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # 找到所有 <item> 元素
    items = root.findall('.//item')

    # 提取每个 <item> 的 <title> 和 <link>
    for item in items:
        
        title = item.find('title').text if item.find('title') is not None else '无标题'
        link = item.find('link').text if item.find('link') is not None else '无链接'
        episode = {"title": title, "link": link}
        # print(f'Title: {title}\nLink: {link}\n')
        fanmai_title_link_list.append(episode)
    return fanmai_title_link_list

# fanmai_ma_title_link_list = get_fanpai_title_link("/opt/lamesbond.github.io/fanpai-film-ma.xml")
fanmai_review_title_link_list = get_fanpai_title_link("/opt/lamesbond.github.io/fanpai-film-review.xml")
# 遍历目录中的每个文件
for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):  # 确保只处理 XML 文件
        file_path = os.path.join(xml_directory, filename)
        
        # 解析 XML 文件
        tree = ET.parse(file_path)
        root = tree.getroot()


        title = root.find('title')
        if title is not None:
            # print(title.text.lower()[:3])
            # print(f'文件: {filename} - 标题: {title.text}')
            for i in fanmai_review_title_link_list:
                # print(i["title"][1:4])

                if i["title"][1:4] == title.text[:3]:
                    print("匹配成功",title.text,i["title"])
                    # 查找所有 <link> 元素并修改其文本
                    for link in root.findall('.//link'):
                        print("link修改为：", i["link"])
                        link.text = i["link"]
        

        # 将修改后的 XML 文件保存
        tree.write(file_path, encoding="UTF-8", xml_declaration=True)

        # print(f'已更新文件: {filename}')
