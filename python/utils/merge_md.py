import os
import re

def get_markdown_files(directory):
    """获取指定目录下所有的markdown文件"""
    return [f for f in os.listdir(directory) if f.endswith('.md')]

def extract_title(content):
    """从markdown内容中提取标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1) if match else "Untitled"

def generate_toc(titles):
    """生成目录"""
    return "\n".join(f"- [{title}](#{title.lower().replace(' ', '-')})" for title in titles)

def merge_markdown_files(directory, output_file):
    files = get_markdown_files(directory)
    titles = []
    content = ""

    for file in files:
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            file_content = f.read()
            title = extract_title(file_content)
            titles.append(title)
            content += f"\n\n# {title}\n\n{file_content}"

    toc = "# Table of Contents\n\n" + generate_toc(titles)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(toc + content)

    print(f"合并完成，输出文件: {output_file}")

# 使用示例
directory = r"C:\path\to\your\markdown\files"  # 替换为您的markdown文件所在的目录
output_file = r"C:\path\to\output\merged_markdown.md"  # 替换为您希望输出的文件路径

merge_markdown_files(directory, output_file)
