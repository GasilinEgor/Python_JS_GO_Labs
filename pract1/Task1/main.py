import re


WORD_PATTERN = r'[a-zA-Zа-яА-ЯёЁ]+'


def check_file(file_name):
    words_dict = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            text = line.strip()
            words = re.findall(WORD_PATTERN, text)
            for word in words:
                lower_word = word.lower()
                if lower_word in words_dict:
                    words_dict[lower_word] += 1
                else:
                    words_dict[lower_word] = 1
    return words_dict
            
            
def main():
    file_name = input("Введите название файла: ")
    words = check_file(file_name)

    sorted_words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
    for word, count in sorted_words.items():
        print(f'{word}: {count}')


if __name__ == '__main__':
    main()