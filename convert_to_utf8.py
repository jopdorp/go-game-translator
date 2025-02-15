import chardet
import sys

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def convert_to_utf8(file_path, detected_encoding):
    with open(file_path, 'r', encoding=detected_encoding, errors='ignore') as f:
        content = f.read()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # passed as argument
    file_path = sys.argv[1]
    detected_encoding = detect_encoding(file_path)
    convert_to_utf8(file_path, detected_encoding)

main()