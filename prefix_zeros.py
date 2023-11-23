#!/usr/bin/env python3
import os
import re
import os
import re
import sys
import openai


def get_max_digits(directory):
    # Get the maximum number of digits in the file names for each directory
    max_digits = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name starts with a number or words followed by a number
            if re.match(r"^(\d+|\w+\s*\d+)", file):
                # Get the number of digits in the file name
                num_digits = len(re.search(r"\d+", file).group())
                # Update the maximum number of digits for the current directory
                max_digits[root] = max(max_digits.get(root, 0), num_digits)
    return max_digits

def prefix_zeros(directory):
    # Get the maximum number of digits for each directory
    max_digits = get_max_digits(directory)

    # Iterate over the files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name starts with a number or words followed by a number
            if re.match(r"^(\d+|\w+\s*\d+)", file):
                # Get the number of digits in the file name, for the first group of digits
                num_digits = len(re.search(r"\d+", file).group())
                # Prefix the file name with the correct amount of zeros
                new_file_name = re.sub(r"\d+", lambda match: match.group().zfill(max_digits[root]), file, count=1)
                # Rename the file
                os.rename(os.path.join(root, file), os.path.join(root, new_file_name))
                translate_comments(os.path.join(root, new_file_name))  

# Find comments in the SGF file
def translate_comments(file_path):
    # Read the file
    with open(file_path, "r") as f:
        file = f.read()
    # Find all comments and their indices
    comments = [(m.group(), m.start(), m.end()) for m in re.finditer(r"C\[(.*?)\]", file, re.DOTALL)]    
    # Translate comments into English and replace the original text
    offset = 0
    for i, (comment, start, end) in enumerate(comments):
        translated_comment = translate_to_english(comment)  # Implement the translation function
        file = file[:start + offset] + translated_comment + file[end + offset:]  # Replace comment at the correct position
        offset += len(translated_comment) - len(comment)  # Update the offset
    
    return file  # Return the translated file instead of the translated comments


def translate_to_english(comment):
    # Set up the OpenAI API credentials
    openai.api_key = "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"

    # Define the Go words and their translations
    go_words_translations = {
        "Go": ["围棋", "Го", "碁"],
        "Ko": ["劫", "Ко", "コウ"],
        "Joseki": ["定石", "Дзосеки", "定石"],
        "Tsumego": ["死活", "Цумего", "詰碁"],
        "Fuseki": ["布局", "Фусеки", "布石"],
        "Sente": ["先手", "Сенте", "先手"],
        "Gote": ["后手", "Готэ", "後手"],
        "Hane": ["挽", "Ханэ", "ハネ"],
        "Atari": ["自摆", "Атари", "アタリ"],
        "Kikashi": ["器差し", "Кикаси", "キカシ"],
        "Dame": ["无气", "Дамэ", "ダメ"],
        "Yose": ["余势", "Ёсэ", "ヨセ"],
        "Sabaki": ["活き", "Сабаки", "サバキ"],
        "Meai": ["目合い", "Мэай", "目合い"],
        "Moyo": ["模样", "Мойо", "モヨ"],
        "Tsuke": ["付け", "Цуке", "ツケ"],
        "Kifu": ["棋谱", "Кифу", "棋譜"],
        "Aji": ["味", "Аджи", "味"],
        "Hoshi": ["星", "Хоси", "星"],
        "Tengen": ["天元", "Тэнгэн", "天元"],
        "Shimari": ["定石角", "Шимари", "シマリ"],
        "Ikken Tobi": ["一间跳", "Иккэн Тоби", "一間飛び"],
        "Sansan": ["三三", "Сансан", "三々"],
        "Niken Tobi": ["二间跳", "Никэн Тоби", "二間飛び"],
        "Yosumi": ["侧对", "Ёсуми", "ヨスミ"],
        "Korigatachi": ["入り角", "Коригатачи", "コリガタチ"],
        # Add more Go words and their translations here
    }


    # Generate the Go words and translations string
    go_words_translations_str = "\n".join([f"{word}: {', '.join(translations)}" for word, translations in go_words_translations.items()])

    # Define the translation prompt
    prompt = f"This is a comment in an SGF file about a game of Go. The comment is: {comment}. Here are some Go words and their translations:\n{go_words_translations_str}"

    # Generate the translation using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for the game of Go."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the translated comment from the response
    translated_comment = response['choices'][0]['message']['content']

    return translated_comment

def main():
    if len(sys.argv) < 2:
        print("Please provide the directory as a command-line argument.")
        return
    directory = sys.argv[1]
    prefix_zeros(directory)


if __name__ == "__main__":
    main()
