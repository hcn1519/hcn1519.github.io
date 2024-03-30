import argparse
import re
from pathlib import Path

class MarkdownListFormatter:
    
    def __init__(self, markdown_file_path: str):
        self.headers = self.extract_headers(markdown_file_path)
        self.number_of_top_header = min([header[1] for header in self.headers])
        self.post_title = self.post_title(markdown_file_path)

    def post_title(self, markdown_file_path) -> str:
        file_name = Path(markdown_file_path).stem
        return file_name.split("-")[-1].replace(" ", "-")

    def extract_headers(self, markdown_file):
        headers = []
        with open(markdown_file, 'r', encoding='utf-8') as file:
            code_open = False
            for line in file:
                if line.startswith("```"):
                    code_open = not code_open
                match = re.match(r'^(#+)\s+(.*)', line)
                if match and not code_open:
                    header_level = len(match.group(1))
                    header_text = match.group(2)
                    headers.append((header_text, header_level))
        return headers

    def indent(self, number_of_pounds: int) -> str:
        tagDiff = number_of_pounds - self.number_of_top_header
        return "    " * tagDiff
    
    def formattedLinkURL(self, target: str) -> str:
        shouldBeRemovedFromURL = [".", ",", "(", ")"]
        formattedURL = target.lower().replace(" ", "-")
        for targetCharacter in shouldBeRemovedFromURL:
            formattedURL = formattedURL.replace(targetCharacter, "") 
        return formattedURL

    def formattedListString(self, indent: str, list_no: int, title: str, link_str: str) -> str:
        return f"{indent}{list_no}. [{title}](./{self.post_title}#{link_str})\n"
    
    def convert_to_markdown_urls(self) -> str:
        merged_str = ""
        counter = [1] * 7
        for sub_title, number_of_pounds in self.headers:
            link_str = self.formattedLinkURL(target=sub_title)
            list_no = counter[number_of_pounds]
            
            merged_str += self.formattedListString(indent=self.indent(number_of_pounds=number_of_pounds),
                                                   list_no=list_no, 
                                                   title=sub_title, 
                                                   link_str=link_str)
            counter[number_of_pounds] += 1

        return merged_str

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Create Table of Content list in markdown URL style")
    parser.add_argument('file_path', type=str, help='Path to the Markdown file')

    args = parser.parse_args()

    formatter = MarkdownListFormatter(args.file_path)
    result = formatter.convert_to_markdown_urls()

    print("## Table of Contents")
    print()
    print(result)