#!/usr/bin/env python3
import os
import re
import os
import re
import sys

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

def prefix_zeros(directory, should_translate=False):
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
                if should_translate:
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
    

    # Define the Go words and their translations
    go_words_translations = {
        "Aji": ["味", "Аджи", "味"],
        "Aji Keshi": ["收味", "Аджи Кэси", "味消し"],
        "Atari": ["自摆", "Атари", "アタリ"],
        "Capturing race": ["争杀", "Гонкакусэн", "取り合い"],
        "Chain": ["串", "Группа", "連"],
        "Connection": ["连接", "Сурунэ", "繋げ"],
        "Cut": ["断", "Кири", "切り"],
        "Dame": ["无气", "Дамэ", "ダメ"],
        "Damezumari": ["死活变化", "Дамэдзумари", "ダメヅマリ"],
        "Death": ["死", "Си", "死"],
        "Dragon": ["龙", "Дракон", "ドラゴン"],
        "Endgame": ["收官", "Эндго", "エンドゲーム"],
        "Eye": ["眼", "Глаз", "目"],
        "False Eye": ["假眼", "Ложное глаз", "偽の目"],
        "Fuseki": ["布局", "Фусеки", "布石"],
        "Geta": ["双三", "Гэта", "ゲタ"],
        "Go": ["围棋", "Го", "碁"],
        "Gote": ["后手", "Готэ", "後手"],
        "Group": ["群", "Группа", "グループ"],
        "Hane": ["挽", "Ханэ", "ハネ"],
        "Handicap": ["让子", "Гандикап", "ハンデ"],
        "Hoshi": ["星", "Хоси", "星"],
        "Ikken Tobi": ["一间跳", "Иккэн Тоби", "一間飛び"],
        "Influence": ["势力", "Инфлюенс", "インフルエンス"],
        "Invasion": ["入侵", "Инвейжн", "インベージョン"],
        "Joseki": ["定石", "Дзосеки", "定石"],
        "Kakari": ["角落", "Какари", "カカリ"],
        "Killing": ["杀", "Киллинг", "キリング"],
        "Kifu": ["棋谱", "Кифу", "棋譜"],
        "Kikashi": ["器差し", "Кикаси", "キカシ"],
        "Ko": ["劫", "Ко", "コウ"],
        "Ko Threat": ["劫威胁", "Ко Тхреат", "コウの脅威"],
        "Komi": ["贴目", "Коми", "コミ"],
        "Liberty": ["气", "Либерти", "呼吸点"],
        "Life": ["活", "Лайф", "ライフ"],
        "Ladder": ["阶梯", "Леддер", "ラダー"],
        "Meai": ["目合い", "Мэай", "目合い"],
        "Moyo": ["模样", "Мойо", "モヨ"],
        "Niken Tobi": ["二间跳", "Никэн Тоби", "二間飛び"],
        "Omoyo": ["大模样", "Омойо", "オモヨ"],
        "Peep": ["窥视", "Пип", "ピープ"],
        "Point": ["点", "Пойнт", "ポイント"],
        "Ponnuki": ["单鬼", "Поннуки", "ポンヌキ"],
        "Sabaki": ["活き", "Сабаки", "サバキ"],
        "Seki": ["均势", "Сэки", "セキ"],
        "Semeai": ["死活争い", "Семэай", "セメアイ"],
        "Semedori": ["死活捕捉", "Семэдори", "セメドリ"],
        "Sente": ["先手", "Сенте", "先手"],
        "Shape": ["形", "Шейп", "シェイプ"],
        "Shicho": ["阶梯", "Шичо", "シチョ"],
        "Shimari": ["定石角", "Шимари", "シマリ"],
        "Soko": ["空", "Соко", "ソコ"],
        "Tengen": ["天元", "Тэнгэн", "天元"],
        "Tenuki": ["手抜き", "Тэнуки", "手抜き"],
        "Territory": ["地", "Территория", "テリトリー"],
        "Tesuji": ["手筋", "Тэсудзи", "テスジ"],
        "Tsuke": ["付け", "Цуке", "ツケ"],
        "Tsumego": ["死活题", "Цумего", "詰碁"],
        "Vital Point": ["要点", "Витал Пойнт", "ビタルポイント"],
        "Yose": ["余势", "Ёсэ", "ヨセ"],
        "Yosumi": ["侧对", "Ёсуми", "ヨスミ"],
        "Zokusuji": ["杂筋", "Зокусудзи", "ゾクスジ"],
        "Zuke": ["付け", "Цуке", "ツケ"],
    }



    # Generate the Go words and translations string
    go_words_translations_str = "\n".join([f"{word}: {', '.join(translations)}" for word, translations in go_words_translations.items()])

    # Define the translation prompt

    # system_message = "You are Orca, an AI language model created by Microsoft. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior."
    # user_message = f"You are a translator, with a specialization in translating text about the game of go into English. You respond with nothing more than the translation.\nHere are some go word translations:\n{go_words_translations_str}\nTranslate the following comment from an SGF file:\n{comment}"
    # prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{user_message}<|im_end|>\n<|im_start|>assistant"

    prompt = f"### Human:\nYou are a translator, with a specialization in translating text about the game of go into English. You respond with nothing more than the translation.\nHere are some go word translations:\n{go_words_translations_str}\nTranslate the following comment from an SGF file:\n{comment}\n\n### ASSISANT:\n"

    inputs = tokenizer(prompt, return_tensors='pt')
    output_ids = model.generate(inputs["input_ids"],)
    answer = tokenizer.batch_decode(output_ids)[0]

    print(answer)

    return answer

def main():
    if len(sys.argv) < 2:
        print("Please provide the directory as a command-line argument.")
        return
    directory = sys.argv[1]
    prefix_zeros(directory)


if __name__ == "__main__":
    main()
