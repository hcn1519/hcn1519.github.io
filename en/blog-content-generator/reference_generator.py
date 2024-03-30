import re
import argparse

def extract_links(markdown_file):
    links = []
    with open(markdown_file, 'r', encoding='utf-8') as file:
        for line in file:
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, line)
            for match in matches:
                link_text, link_url = match
                links.append((link_text, link_url))
    return links

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Create Table of Content list in markdown URL style")
    parser.add_argument('file_path', type=str, help='Path to the Markdown file')

    args = parser.parse_args()
    
    extracted_links = extract_links(args.file_path)
    
    merged_str = ""
    for link_text, link_url in extracted_links:

        if link_url.startswith("https"):
            merged_str += f"- [{link_text}]({link_url})\n"

    print("# 참고자료")
    print(merged_str)
